import psycopg

from core.config import config

conninfo = f"user={config.DATABASE_USER} password={config.DATABASE_PASSWORD} host={config.DATABASE_HOST} port={config.DATABASE_PORT} dbname={config.DATABASE_DBNAME}"


def get_connection():
    return psycopg.connect(conninfo)
