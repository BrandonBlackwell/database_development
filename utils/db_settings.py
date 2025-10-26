from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ConfigDict as SettingsConfigDict, model_validator

class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    db_host_prod: str
    db_port_prod: int
    db_name_prod: str
    db_user_prod: str
    db_password_prod: str
    db_url_string_prod: Optional[str]=None
    db_host_dev: str
    db_port_dev: int
    db_name_dev: str
    db_user_dev: str
    db_password_dev: str
    db_url_string_dev: Optional[str]=None
    db_host_test: str
    db_port_test: int
    db_name_test: str
    db_user_test: str
    db_password_test: str
    db_url_string_test: Optional[str]=None
    
    @model_validator(mode='after')
    def validate_ports(self):
        return self

if __name__ == "__main__":    
    db_settings = DatabaseSettings()
    print("Development Database Settings:")
    print(db_settings.db_name_dev)
    print("Production Database Settings:")
    print(db_settings.db_name_prod)