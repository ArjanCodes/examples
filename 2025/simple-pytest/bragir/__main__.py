import click

from bragir import commands
from bragir.client import initate_async_client
from bragir.config import create_config_file, get_config
from bragir.tracing.logger import setup_logging, logger
from bragir.tracing.stratergies import InfoLoggerStrategy

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.pass_context
@click.version_option()
def cli(context: click.Context) -> None:
    """
    Bragir is an tool that can generate SRT files from videos and translate SRT files.

    In order to use Bragir, an OpenAI api_key needs to be passed as an option. Or alternativly,
    as an enviroment variable in the current session
    """

    setup_logging(InfoLoggerStrategy())

    config = get_config()

    if config is None and context.invoked_subcommand == "config":
        logger.info("Config file not found")
        create_config_file()
        exit(0)

    if config is None:
        logger.error("Config file not found")
        logger.info(
            "Run the following command to create a new config file: `bragir config create`"
        )
        exit(1)

    context.ensure_object(dict)
    if not context.invoked_subcommand == "config":
        api_key: str = config.client.openai_api_key

        # TODO: Fix so the check does not always run, for example when calling the config commands
        # client = initiate_client(api_key=api_key)
        client = initate_async_client(api_key=api_key)

        context.obj["client"] = client

    context.obj["config"] = config


cli.add_command(commands.transcribe)
cli.add_command(commands.translate)
cli.add_command(commands.config)
