import os
from logging.config import fileConfig

from alembic import context
from app.config import Environment, settings
from app.db.connectors import connect_to_db, connect_to_local_db
from app.db.models import Base
from dotenv import load_dotenv

load_dotenv()

# When using local development, use the service account credentials
if settings.ENVIRONMENT == Environment.DEVELOPMENT.value:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "../service-account.json"
    )


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata
# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    if settings.ENVIRONMENT == Environment.PRODUCTION.value:
        connectable, session = connect_to_db()
    else:
        connectable, session = connect_to_local_db()

    session.begin()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema="leadspotr",
            include_schemas=True,
        )

        with context.begin_transaction():
            context.execute("SET search_path TO leadspotr")
            context.run_migrations()


run_migrations_online()
