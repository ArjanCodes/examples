import click

from bragir.client import initiate_client
from bragir.config import LoggingLevel, config
from bragir.tracing.logger import setup_logging
from bragir.tracing.stratergies import DebugLoggerStrategy, InfoLoggerStrategy

from . import commands


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.pass_context
@click.version_option()
@click.option(
    "logging_level",
    "--logging_level",
    "-ll",
    type=click.Choice(["info", "debug"], case_sensitive=False),
    help="Use the log level",
)
def cli(context: click.Context, logging_level: str):
    """
    Bragir is an tool that can generate SRT files from videos and translate SRT files.

    In order to use Bragir, an OpenAI api_key needs to be passed as an option. Or alternativly,
    as an enviroment variable in the current session
    """

    context.ensure_object(dict)

    api_key: str = config.client.openai_api_key.get_secret_value()

    client = initiate_client(api_key=api_key)

    context.obj["client"] = client

    if not logging_level:
        logging_level = config.logging.level

    logging_level = logging_level.upper()
    if logging_level == "INFO":
        setup_logging(InfoLoggerStrategy())
    elif logging_level == "DEBUG":
        setup_logging(DebugLoggerStrategy())

    config.logging.level = LoggingLevel[logging_level]
    context.obj["config"] = config


cli.add_command(commands.transcribe)
cli.add_command(commands.translate)
