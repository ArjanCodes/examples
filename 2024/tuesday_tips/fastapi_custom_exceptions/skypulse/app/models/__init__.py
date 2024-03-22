from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


from .city import City  # type: ignore # noqa
from .weather import Weather  # type: ignore # noqa
