# storeapi/logtail_handler.py
import logging
import queue
import threading
from typing import Any, Dict
from datetime import datetime, timezone

import requests
from pythonjsonlogger import jsonlogger

DEFAULT_TIMEOUT = 5  # seconds
BATCH_FLUSH_INTERVAL = 1.0  # seconds
MAX_QUEUE_SIZE = 10000


class BetterStackHandler(logging.Handler):
    """
    Non-blocking logging handler that sends logs to BetterStack / Logtail HTTP ingest endpoint.
    It batches events in-memory and flushes them periodically on a background thread.
    """

    def __init__(
        self,
        endpoint: str,
        source_token: str,
        service_name: str = "unknown-service",
        flush_interval: float = BATCH_FLUSH_INTERVAL,
        timeout: int = DEFAULT_TIMEOUT,
        queue_size: int = MAX_QUEUE_SIZE,
    ):
        super().__init__()
        self.endpoint = endpoint.rstrip("/")  # e.g. https://.../v1/logs
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {source_token}",
        }
        self.service_name = service_name
        self.timeout = timeout
        self._queue: "queue.Queue[Dict[str, Any]]" = queue.Queue(maxsize=queue_size)
        self.flush_interval = flush_interval
        self._stop_event = threading.Event()
        self._worker = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker.start()
        # Use python-json-logger's JsonFormatter if you like
        self.json_formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s"
        )

    def emit(self, record: logging.LogRecord) -> None:
        try:
            # let any formatting/filtering happen first
            msg = self.format(record)
            event = self._make_event(record, msg)
            try:
                self._queue.put_nowait(event)
            except queue.Full:
                # drop on overflow to keep app responsive
                return
        except Exception:
            self.handleError(record)

    def _make_event(
        self, record: logging.LogRecord, rendered_message: str
    ) -> Dict[str, Any]:
        # Build structured event according to BetterStack expected fields.
        # Include common extras that you use (correlation_id, email, trace_id, span_id, etc.)
        event = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=timezone.utc
            ).isoformat(),
            "level": record.levelname,
            "message": rendered_message,
            "logger": record.name,
            "service": self.service_name,
            # include any available extra fields
        }
        # Attach extras that libraries place on the record, be defensive
        for key in ("correlation_id", "email", "trace_id", "span_id", "some_key"):
            if hasattr(record, key):
                event[key] = getattr(record, key)
        # include record.__dict__ extras (avoid builtin names)
        extras = {
            k: v
            for k, v in record.__dict__.items()
            if k
            not in (
                "name",
                "msg",
                "args",
                "levelname",
                "levelno",
                "pathname",
                "filename",
                "module",
                "exc_info",
                "exc_text",
                "stack_info",
                "lineno",
                "funcName",
                "created",
                "msecs",
                "relativeCreated",
                "thread",
                "threadName",
                "processName",
                "process",
            )
        }
        if extras:
            event["extras"] = extras
        return event

    def _flush_batch(self, batch: list[Dict[str, Any]]) -> None:
        if not batch:
            return
        try:
            # BetterStack accepts a single event or a list — we send list of events
            payload = batch if len(batch) > 1 else batch[0]
            resp = requests.post(
                self.endpoint,
                headers=self.headers,
                json=payload,
                timeout=self.timeout,
            )
            # Accept 2xx success:
            if resp.status_code >= 400:
                # Optionally log locally on error, but don't retry forever here
                # Use self.handleError to surface if needed
                pass
        except Exception:
            # swallow any exception: do not crash app
            return

    def _worker_loop(self) -> None:
        buffer = []
        while not self._stop_event.is_set():
            try:
                # block for short interval waiting for items
                item = None
                try:
                    item = self._queue.get(timeout=self.flush_interval)
                except queue.Empty:
                    pass

                if item is not None:
                    buffer.append(item)
                    # try to collect a small batch quickly
                    while True:
                        try:
                            item = self._queue.get_nowait()
                            buffer.append(item)
                        except queue.Empty:
                            break

                if buffer:
                    # flush
                    self._flush_batch(buffer)
                    buffer.clear()
            except Exception:
                # avoid crashing worker thread
                continue

    def close(self) -> None:
        self._stop_event.set()
        self._worker.join(timeout=2.0)
        # flush remaining
        remaining = []
        while not self._queue.empty():
            try:
                remaining.append(self._queue.get_nowait())
            except queue.Empty:
                break
        if remaining:
            self._flush_batch(remaining)
        super().close()
