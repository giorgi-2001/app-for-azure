import logging

from opencensus.ext.azure.log_exporter import AzureLogHandler
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


VAULT_URL = "https://learn-azure-kw.vault.azure.net/"
SECRET_NAME = "app-insights-inst-key"


credential = DefaultAzureCredential()
client = SecretClient(vault_url=VAULT_URL, credential=credential)
inst_key = client.get_secret(SECRET_NAME).value

connection_string = f"InstrumentationKey={inst_key}"


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


logger.addHandler(AzureLogHandler(connection_string=connection_string))


stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter(
    '{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
))
logger.addHandler(stream_handler)
