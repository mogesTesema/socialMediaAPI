import logging
from functools import lru_cache #noqa
import b2sdk.v2 as b2
from b2sdk.v2.account_info import InMemoryAccountInfo
from foodapp.core.config import get_file_upload_keys

logger = logging.getLogger(__name__)

b2_key_set = get_file_upload_keys()


@lru_cache()
def b2_api():
    logger.debug("creating and authorize B2 API")
    info = InMemoryAccountInfo()
    b2_api = b2.B2Api(info)
    b2_api.authorize_account(
        "production", b2_key_set.B2_KEY_ID, b2_key_set.B2_APPLICATION_KEY
    )

    return b2_api


@lru_cache()
def b2_get_bucket(api: b2.B2Api):
    return api.get_bucket_by_name(b2_key_set.B2_BUCKET_NAME)


def b2_upload_file(local_file: str, file_name: str) -> str:
    api = b2_api()
    logger.debug(f"Uploading {local_file}to B2 as {file_name}")

    uploaded_file = b2_get_bucket(api).upload_local_file(
        local_file=local_file, file_name=file_name
    )

    download_url = api.get_download_url_for_fileid(uploaded_file.id_)
    logger.debug(
        f"Upload {local_file} to B2 successfully and got download URL {download_url}"
    )

    return download_url
