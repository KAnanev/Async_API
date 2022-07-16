import pathlib

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()


class TestSettings(BaseSettings):
    REDIS_HOST: str = Field('redis')
    REDIS_PORT: int = Field(6379)
    ELASTIC_HOST: str = Field('elastic')
    ELASTIC_PORT: int = Field(9200)
    API_HOST: str = Field('http://127.0.0.1')
    API_PORT: str = Field(8000)
    API_VERSION: str = Field('v1')

    class Config:
        env_file = pathlib.Path(__file__).parent.parent.resolve() / '.env'


settings = TestSettings()
