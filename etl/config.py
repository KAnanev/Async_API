import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(funcName)s - %(message)s",
    handlers=[
        logging.StreamHandler(
            sys.stdout
        ),
        RotatingFileHandler(
            filename="{}/elastic.log".format(os.path.dirname(os.path.abspath(__file__))),
            maxBytes=10000000,
            backupCount=10)]
    )

logger = logging.getLogger()

index_names = ('movies', 'persons', 'genres')

state_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'state', '') + 'state.json'

pg_conf = {
    'dbname': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST'),
    'port': os.getenv('POSTGRES_PORT')
}

es_conf = [{
    'host': os.getenv('ELASTIC_HOST'),
    'port': os.getenv('ELASTIC_PORT'),
}]
