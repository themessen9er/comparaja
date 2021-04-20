import os

# Read Secrets from protected files as well as db-related Env vars.

with open(os.environ['POSTGRES_USER_FILE'], "r") as f:
    _username = f.readline()

with open(os.environ['POSTGRES_PASSWORD_FILE'], "r") as f:
    _password = f.readline()

_server = os.environ.get("POSTGRES_DB_SERVER", "db")
_port = os.environ.get("POSTGRES_DB_PORT", "5432")
_db_name = os.environ["POSTGRES_DB"]

DATABASE_CONNECTION_STRING = "postgres://{}:{}@{}:{}/{}".format(
    _username, _password, _server, _port, _db_name
)