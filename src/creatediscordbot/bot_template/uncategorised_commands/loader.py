import logging

from importlib import import_module

from settings import UNCATEGORISED_COMMANDS_DIR
logger = logging.getLogger(__name__)


def load_uncategorised_commands(bot):
    """
    Loads uncategorised commands dynamically from command file in uncategorised commands folder, set by settings
    Commands need to be named the same as the file

    Example:
    test.py -> command is test()

    Has to be used with discordpy ext commands

    :param bot:
    :return:
    """
    # create list to keep track of loaded commands for debug and info
    commands_list = list()
    # go over all .py files in the uncategorised commands folder
    for file_item in UNCATEGORISED_COMMANDS_DIR.rglob("*.py"):
        # we get Pathlib Path objects
        filename = file_item.name
        # Ignore everything that is not a file, this file or starts with _
        if filename.startswith("_") or filename == "loader.py" or not file_item.is_file():
            continue

        # get the bare name, command has to be named same as filename
        command_import_name = filename[:-3]
        try:
            # notify developer which command is being loaded
            logger.debug(
                f'Loading Uncategorised Command: {command_import_name} from {filename=}')

            # dynamically import module, from relative path to this module!
            module = import_module(
                f'.{command_import_name}', package='uncategorised_commands')

            # get the actuall command function dynamically
            command = getattr(module, command_import_name)

            # add the command to the bot
            bot.add_command(command)

            # keep track
            commands_list.append(command_import_name)
        except (AttributeError, TypeError) as e:
            # AttributeError happens when there is no method with the same name as the python filename
            # TypeError if the command method in the file exists, but does not use @commands.command()
            logger.error(
                f'{str(e)} :: occured with command: {command_import_name} in {filename=}')

    # log information about which and how many commands have been loaded
    commands_count = len(commands_list)
    if commands_count > 0:
        logger.info(f"Loaded {len(commands_list)} uncategorised commands")
        logger.debug(f'Full list of dynamic commands: {commands_list}')
    else:
        logger.info("No uncategorised commands found or loaded")
