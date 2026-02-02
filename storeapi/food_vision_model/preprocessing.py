"""
Preprocessing utilities for food vision inputs.
"""

from __future__ import annotations

import io
import zipfile
from pathlib import Path
from typing import List, Sequence, Tuple, Union

import numpy as np
from PIL import Image


ImageInput = Union[str, Path, bytes, Image.Image]


def _load_image(image: ImageInput) -> Image.Image:
	if isinstance(image, (str, Path)):
		try:
			return Image.open(image)  # type: ignore[arg-type]
		except Exception as exc:
			raise ValueError(f"invalid image file: {exc}") from exc
	if isinstance(image, (bytes, bytearray)):
		try:
			return Image.open(io.BytesIO(image))  # type: ignore[arg-type]
		except Exception as exc:
			raise ValueError(f"invalid image file: {exc}") from exc
	if isinstance(image, Image.Image):
		return image
	raise TypeError("image must be a path, bytes, or PIL.Image.Image")


def prepare_image(
	image: ImageInput,
	input_shape: Sequence[object],
	input_dtype: np.dtype,
) -> np.ndarray:
	image = _load_image(image).convert("RGB")

	if len(input_shape) != 4:
		raise ValueError(f"Unexpected input shape: {input_shape}")

	shape = [s if isinstance(s, int) else None for s in input_shape]
	if shape[1] == 3:
		layout = "NCHW"
		height = shape[2] or image.height
		width = shape[3] or image.width
	else:
		layout = "NHWC"
		height = shape[1] or image.height
		width = shape[2] or image.width

	image = image.resize((int(width), int(height)))
	array = np.asarray(image)

	# Model expects raw pixel values (no rescaling). Cast to float32 if needed.
	if np.issubdtype(input_dtype, np.floating):
		array = array.astype(np.float32)
	else:
		array = array.astype(input_dtype)

	if layout == "NCHW":
		array = np.transpose(array, (2, 0, 1))

	# Always return a batch of 1 for inference.
	return np.expand_dims(array, axis=0)


def prepare_batch(
	images: Sequence[ImageInput],
	input_shape: Sequence[object],
	input_dtype: np.dtype,
) -> np.ndarray:
	if not images:
		raise ValueError("images must contain at least one item")

	batch = []
	for image in images:
		prepared = prepare_image(image, input_shape, input_dtype)
		batch.append(np.squeeze(prepared, axis=0))

	return np.stack(batch, axis=0)


def decode_zip_images(
	zip_bytes: bytes,
	max_images: int = 32,
) -> Tuple[List[str], List[bytes]]:
	if not zip_bytes:
		raise ValueError("uploaded file is empty")

	try:
		zip_buffer = io.BytesIO(zip_bytes)
		with zipfile.ZipFile(zip_buffer) as zip_file:
			names = [
				name
				for name in zip_file.namelist()
				if not name.endswith("/")
			]
			if not names:
				raise ValueError("zip contains no files")
			if len(names) > max_images:
				raise ValueError(f"maximum {max_images} images allowed per zip")
			images = [zip_file.read(name) for name in names]
			return names, images
	except zipfile.BadZipFile as exc:
		raise ValueError(f"invalid zip file: {exc}") from exc
