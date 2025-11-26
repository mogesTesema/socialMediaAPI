from pydantic_settings import BaseSettings
from typing import Optional

class BaseConfig(BaseSettings):
    ENV_STATE: Optional[str] = None
    class Config:
        env_file:str = ".env"

class GlobalConfig(BaseConfig):
    DATABASE_URL: Optional[str] =None
    DB_FORCE_ROLL_BACK: bool = False


class DevConfig(GlobalConfig):

    class Config:
        env_prefix: str = "DEV_"

class ProdConfig(GlobalConfig):
    
    class Config:
        env_prefix: str = "PROD_"


class TestConfig(GlobalConfig):
    
    class Config:
        env_prefix: str = "TEST_"