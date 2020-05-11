import os
import sys
import shutil
import subprocess

from colorama import init

from .utils import *
from .templater import *

init()

LIBRARY_FOLDER = os.path.dirname(os.path.abspath(__file__))

# Folder Names
BOT_TEMPLATES_FOLDER_NAME = 'bot_template'
DOCKER_TEMPLATES_FOLDER_NAME = "docker_templates"
COG_TEMPLATES_FOLDER_NAME = 'cog_template'
UNCATEGORISED_COMMANDS_FOLDER_NAME = "uncategorised_commands"

# Library Folder Paths
BOT_TEMPLATES_FOLDER = os.path.join(LIBRARY_FOLDER, BOT_TEMPLATES_FOLDER_NAME)


def read_cwd():
    """
    Gets the current working directory when initalising the bot
    :return:
    """
    # Take the current directory for creating the bot
    cwd = os.getcwd()

    cwd_input = input(f"Where do you want to initialise the bot? ({cwd}):")
    if not os.path.isdir(cwd_input) and cwd_input != "":
        error(f"{cwd_input} is not a directory.")
        return
    else:
        if cwd_input == "":
            pass
        else:
            # take the user input as working directory
            cwd = cwd_input
    return cwd


def create_cog(cog_name="", bot_project_location="", with_tests=False, bare=False):
    """
    Creates a new Cog based on template
    :param cog_name:
    :param bot_project_location:
    :param initial:
    :return:
    """
    if cog_name == "":
        return

    # Create the cog folder name, and create the path where the folder should be located
    final_cog_name = clean_cog_name(cog_name)

    # Cog Location = Where to save the Cog
    cog_location = os.path.join(bot_project_location, 'cogs', final_cog_name)

    # check if the cog already exists. if so, abort!
    if check_if_folder_exists(cog_location):
        error("Already have a Cog with this name.")
        return

    # create cog folder based on name
    os.mkdir(cog_location)

    if bare:
        cog_template = "cog_bare.py-temp"
    else:
        cog_template = "cog_full.py-temp"

    # create cog file itself, from template
    cog_template_file_name = os.path.join(LIBRARY_FOLDER, COG_TEMPLATES_FOLDER_NAME, cog_template)
    cog_file = os.path.join(cog_location, f"{final_cog_name}.py")

    replace_cog_placeholder(final_cog_name, cog_template_file_name, cog_file)

    # create empty init py file
    with open(os.path.join(cog_location, "__init__.py"), "w"):
        pass

    # check if bare
    if not bare:
        # create controller, model, converter and tests folder
        controller_template_file_name = os.path.join(LIBRARY_FOLDER, COG_TEMPLATES_FOLDER_NAME, "controller.py-temp")

        controller_file = os.path.join(cog_location, "controller.py")

        replace_controller_placeholder(final_cog_name, controller_template_file_name=controller_template_file_name,
                                       controller_file=controller_file)

        # copy model file
        model_template_file = os.path.join(LIBRARY_FOLDER, COG_TEMPLATES_FOLDER_NAME, "model.py")
        project_model_file = os.path.join(cog_location, "model.py")

        shutil.copyfile(model_template_file, project_model_file)

        # copy converter file
        converter_template_file = os.path.join(LIBRARY_FOLDER, COG_TEMPLATES_FOLDER_NAME, "converter.py")
        project_converter_file = os.path.join(cog_location, "converter.py")

        shutil.copyfile(converter_template_file, project_converter_file)

        if with_tests:
            # create folder
            os.mkdir(os.path.join(cog_location, "tests"))

            # create empty init py file
            with open(os.path.join(cog_location, "tests", "__init__.py"), "w"): pass

            # create controller test file
            with open(os.path.join(cog_location, "tests", "test_controller.py"), "w"): pass
            # create model test file
            with open(os.path.join(cog_location, "tests", "test_model.py"), "w"): pass
            # create converter test file
            with open(os.path.join(cog_location, "tests", "test_converter.py"), "w"): pass

    success("Full Cog was successfully created.")


def create_uncategorised_command(command_name, path=None):
    """
    Creates an uncagetorised command
    :param command_name:
    :return:
    """
    # don't do anything if we do not have the path for the uncategorised commands folder
    if path is None:
        error("No uncategorised commands folder set")
        return

    # clean the name
    final_command_name = clean_command_name(command_name)
    if not final_command_name or final_command_name == "loader":
        error("Please make sure you alphanumeric for commands")
        return

    # get the template path for our command in the library
    template_path = os.path.join(LIBRARY_FOLDER, BOT_TEMPLATES_FOLDER_NAME, UNCATEGORISED_COMMANDS_FOLDER_NAME,
                                 "command.py-temp")

    # get the final output path
    final_file = os.path.join(path, f"{final_command_name}.py")

    # replace the template
    result = replace_uncategorised_command_placeholder(final_command_name, template_path, final_file)
    if result:
        success(f"Created uncategorised command {final_command_name}")
    else:
        error(f"Could not create uncategorised command: {final_command_name}")


def create_docker_compose_dev_file(root_folder, project_folder, docker_compose_dev_template):
    """
    Create docker-compose-dev.yml Development file
    :param root_folder:
    :param project_folder:
    :param docker_compose_dev_template:
    :return:
    """
    docker_compose_dev_file = os.path.join(root_folder, "docker-compose-dev.yml")

    # Make sure user doesn't overwrite their existing docker file
    if os.path.exists(docker_compose_dev_file):
        user_overwrite = input(
            "A docker-compose-dev.yml already exists in the root folder. Do you want to overwrite it? N/y (Default No): ")
        if user_overwrite.lower() != "y":
            return

    prod_result = replace_docker_compose_placeholder(project_folder, docker_compose_dev_template,
                                                     docker_compose_dev_file)
    if prod_result:
        success("Created docker-compose-dev.yml file")
    else:
        error("Could not create docker-compose-dev.yml file")
        return


def create_docker_compose_prod_file(root_folder, project_folder, docker_compose_prod_template):
    """
    create docker-compose.yml Production File
    :param root_folder:
    :param project_folder:
    :param docker_compose_prod_template:
    :return:
    """

    docker_compose_prod_file = os.path.join(root_folder, "docker-compose.yml")

    # Make sure user doesn't overwrite their existing docker file
    if os.path.exists(docker_compose_prod_file):
        user_overwrite = input(
            "A docker-compose.yml already exists in the root folder. Do you want to overwrite it? N/y (Default No): ")
        if user_overwrite.lower() != "y":
            return

    prod_result = replace_docker_compose_placeholder(project_folder, docker_compose_prod_template,
                                                     docker_compose_prod_file)
    if prod_result:
        success("Created docker-compose.yml file")
    else:
        error("Could not create docker-compose.yml file")
        return


def create_dockerfile(project_folder, dockerfile_project_template):
    """
    Create Dockerfile for both cases inside the actual bot folder
    :param project_folder:
    :param dockerfile_project_template:
    :return:
    """

    docker_file = os.path.join(project_folder, "Dockerfile")
    # Make sure user doesn't overwrite their existing docker file
    if os.path.exists(docker_file):
        user_overwrite = input(
            "A Dockerfile already exists in the bot folder. Do you want to overwrite it? N/y (Default No): ")
        if user_overwrite.lower() != "y":
            return

    prod_result = replace_dockerfile_placeholder(project_folder, dockerfile_project_template,
                                                 docker_file)
    if prod_result:
        success("Created Dockerfile inside bot folder")
    else:
        error("Could not create Dockerfile in bot folder")
        return


def make_docker(project_folder):
    """
    Creates the docker files
    :param project_folder:
    :return:
    """
    # Setup the template files
    docker_compose_prod_template = os.path.join(LIBRARY_FOLDER, DOCKER_TEMPLATES_FOLDER_NAME, "docker-compose.yml-temp")
    docker_compose_dev_template = os.path.join(LIBRARY_FOLDER, DOCKER_TEMPLATES_FOLDER_NAME,
                                               "docker-compose-dev.yml-temp")
    dockerfile_project_template = os.path.join(LIBRARY_FOLDER, DOCKER_TEMPLATES_FOLDER_NAME, "Dockerfile.temp")

    # get the root folder of the bot, not the bot folder itself
    root_folder = os.path.dirname(project_folder)

    # create docker-compose prod file
    create_docker_compose_prod_file(root_folder, project_folder, docker_compose_prod_template)

    # create docker-compose dev file
    create_docker_compose_dev_file(root_folder, project_folder, docker_compose_dev_template)

    # create Dockerfile in bot folder
    create_dockerfile(project_folder, dockerfile_project_template)


def create_bot(bot_name=""):
    """
    Creates a new Discord Bot
    :param bot_name:
    :return:
    """
    if bot_name == "":
        return

    # Get the cwd where bot should be initialised in
    cwd = read_cwd()

    # parse the bot name
    final_bot_name = clean_bot_name(bot_name)

    # check if the bot with this name exists...if so abort!
    if check_if_folder_exists(final_bot_name):
        error("Already have a bot with this name")
        return

    # set the path where the bot will be installed in
    final_path = os.path.join(cwd, final_bot_name)

    # copy the bot template over
    p("Copying template files to bot folder... this might take a few seconds")
    shutil.copytree(BOT_TEMPLATES_FOLDER, final_path)

    # create logs folder
    os.mkdir(os.path.join(cwd, "logs"))

    # create initial cog as well
    p("Creating initial Cog with same name as bot name")
    create_cog(final_bot_name, final_path, with_tests=True)

    # remove the __init__.py file from the final bot directory
    os.remove(os.path.join(final_path, "__init__.py"))

    # remove uncategorised_commands command template file
    os.remove(os.path.join(final_path, UNCATEGORISED_COMMANDS_FOLDER_NAME, "command.py-temp"))

    # write a config file with initial settings, that user can change for further commands
    p("Writing config file")
    config = {
        "DEFAULT": {
            "PROJECT_ROOT": final_path,
            "COG_BARE_DEFAULT": False,
            "COG_CREATE_UNITTESTS_DEFAULT": True,
            "UNCATEGORISED_COMMANDS_DIR": os.path.join(final_path, UNCATEGORISED_COMMANDS_FOLDER_NAME),
        },

    }
    save_config(config)

    success("Finished! You can now start working on your bot.")


def run(args):
    """
    Parse user arguments and check which command to call
    Command have to be the first passed argument
    
    """
    if len(args) == 0:
        print("Please use --help")

    cmd = args[1]

    if cmd == "--help" or cmd == "-h":
        print_help()

    elif cmd == 'createcommand':
        config = read_config()
        uncategorised_command_dir = config['DEFAULT']['uncategorised_commands_dir']
        create_uncategorised_command(args[2], uncategorised_command_dir)
    elif cmd == 'createcog':
        config = read_config()
        bare = config['DEFAULT'].getboolean("cog_bare_default")
        with_tests = config['DEFAULT'].getboolean("cog_create_unittests_default")
        if len(args) > 3:
            # we should have flags
            if "--bare" in args:
                bare = True
            if "--tests" in args:
                with_tests = False

        create_cog(args[2], config['DEFAULT']['project_root'], bare=bare, with_tests=with_tests)

    elif cmd == 'createbot':
        if sys.argv[2]:
            create_bot(args[2])
        else:
            p("Please specify the name of the bot, or use --help")

    elif cmd == 'makedocker':
        config = read_config()
        make_docker(config['DEFAULT']['project_root'])

    else:
        print_help()
