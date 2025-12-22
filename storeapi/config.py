from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from functools import lru_cache


class BaseConfig(BaseSettings):
    ENV_STATE: Optional[str] = None
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class GlobalConfig(BaseConfig):
    DATABASE_URL: Optional[str] = None
    DB_FORCE_ROLL_BACK: bool = False
    LOGTAIL_HOST: Optional[str] = None
    LOGTAIL_SOURCE_TOKEN: Optional[str] = None
    BREVO_API_KEY: Optional[str] = None
    BREVO_SENDER: Optional[str] = None


class DevConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="DEV_", extra="ignore")


class ProdConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="PROD_", extra="ignore")


class TestConfig(GlobalConfig):
    DB_FORCE_ROLL_BACK: bool = True
    model_config = SettingsConfigDict(env_prefix="TEST_", extra="ignore")


class SecurityKeys(BaseConfig):
    SECRET_KEY: Optional[str] = None
    ALGORITHM: Optional[str] = None
    REFRESH_TOKEN_SECRET_KEY: Optional[str] = None
    REFRESH_TOKEN_ALGORITHM: Optional[str] = None
    SENTRY_DSN:Optional[str]=None
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class FileUploadKeys(BaseSettings):
    B2_KEY_ID: Optional[str] = None
    B2_APPLICATION_KEY: Optional[str] = None
    B2_BUCKET_NAME: Optional[str] = None
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


def get_file_upload_keys():
    return FileUploadKeys()


def get_secrets():
    return SecurityKeys()


@lru_cache()
def get_config(env_state: str):
    configs = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
    return configs.get(env_state, DevConfig)()


config = get_config(BaseConfig().ENV_STATE)
