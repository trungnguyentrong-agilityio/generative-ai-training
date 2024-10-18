from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from e_commerce_chatbot import settings

def get_db_engine(read_only=False):
    """
    Get the database engine.

    Args:
        read_only: Whether the engine is read-only.

    Returns:
        The database engine.
    """

    db_user = settings.postgres_user
    db_password = settings.postgres_password
    db_name = settings.postgres_db
    db_host = settings.postgres_host
    db_port = settings.postgres_port

    if read_only:
        # Use a read-only role or user
        db_user = settings.postgres_read_only_user
        db_password = settings.postgres_read_only_password
        
        # Optionally, you can set session variables to enforce read-only mode
        connect_args = {
            "options": "-c default_transaction_read_only=on"
        }
    else:
        connect_args = {}

    url = URL.create(
        drivername="postgresql+psycopg2",
        username=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
        database=db_name
    )

    return create_engine(url, connect_args=connect_args)
