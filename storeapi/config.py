from pydantic_settings import BaseSettings,SettingsConfigDict
from typing import Optional
from functools import lru_cache

class BaseConfig(BaseSettings):
    ENV_STATE: Optional[str] = None
    model_config = SettingsConfigDict(env_file=".env",extra="ignore")
    

class GlobalConfig(BaseConfig):
    DATABASE_URL: Optional[str] =None
    DB_FORCE_ROLL_BACK: bool = False


class DevConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="DEV_",extra="ignore")

class ProdConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="PROD_",extra="ignore")


class TestConfig(GlobalConfig):
    DB_FORCE_ROLL_BACK: bool = True 
    model_config = SettingsConfigDict(env_prefix="TEST_",extra="ignore")

@lru_cache() 
def get_config(env_state:str):
      configs = {"dev":DevConfig, "prod":ProdConfig, "test":TestConfig}
      return configs[env_state]()

config = get_config(BaseConfig().ENV_STATE)
 