import logging
import os

from dotenv import load_dotenv

from opencensus.ext.azure.log_exporter import AzureLogHandler


load_dotenv()


CONNECTION_STRING = os.getenv(
    "APP_INSIGHT_CONN_STR"
)

print(CONNECTION_STRING)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


logger.addHandler(AzureLogHandler(connection_string=CONNECTION_STRING))


stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter(
    '{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
))
logger.addHandler(stream_handler)
