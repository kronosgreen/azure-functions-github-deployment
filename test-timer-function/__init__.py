import logging
import datetime

import azure.functions as func

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

from urllib.parse import quote_plus as urlquote
from sqlalchemy import create_engine


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    vault_url = 'https://dashboard-test-keys.vault.azure.net/'
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)

    engine = 'postgresql+psycopg2'
    user = client.get_secret('test-db-user').value
    password = client.get_secret('test-db-pass').value
    host = client.get_secret('test-db-host').value
    db = 'test-db'

    connection_url = '%s://%s:%s@%s/%s?sslmode=require' % \
        (engine, user, urlquote(password), host, db)

    print("Connecting to database...")
    db_engine = create_engine(connection_url)

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
