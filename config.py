from pydantic_settings import BaseSettings


class Config(BaseSettings):
    TOKEN: str
    APP_ID: str

    class Config:
        env_file = '.env'


config = Config()
