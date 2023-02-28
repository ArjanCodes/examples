import logging
import sys
from logging.handlers import SysLogHandler

PAPERTRAIL_HOST = "logs.papertrailapp.com"
PAPERTRAIL_PORT = 37554


def main() -> None:
    logger = logging.getLogger("arjancodes")
    logger.setLevel(logging.DEBUG)
    handler = SysLogHandler(address=(PAPERTRAIL_HOST, PAPERTRAIL_PORT))
    logger.addHandler(handler)

    logger.debug("This is a debug message.")


if __name__ == "__main__":
    main()
