from pydantic import SettingsModel, BaseModel
from pydantic_settings import BaseSettings

class DatabaseSettings(BaseModel):
    db_host: str
    db_port: int
    db_username: str
    db_password: str
    db_database_name: str
    
class Settings(BaseSettings):
    SettingsModel(env_file='.env')
    dev_database: DatabaseSettings
    prod_database: DatabaseSettings

if __name__ == "__main__":    
    settings = Settings()
    print("Development Database Settings:")
    print(settings.dev_database)
    print("Production Database Settings:")
    print(settings.prod_database)