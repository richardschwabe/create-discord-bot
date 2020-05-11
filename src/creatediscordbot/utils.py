import os
import re
import configparser

from colorama import Fore, Back, Style


def clean_bot_name(bot_name):
    """
    Cleans the bot name
    :param bot_name:
    :return:
    """
    final_bot_name = bot_name.lower().replace(" ", "_").strip()
    final_bot_name = re.sub("[\W_-]", "", final_bot_name)
    return final_bot_name


def clean_cog_name(cog_name):
    """
    Cleans Cog Name
    :param cog_name:
    :return:
    """
    final_cog_name = cog_name.lower().replace(" ", "_").strip()
    final_cog_name = re.sub("[\W_-]", "", final_cog_name)
    return final_cog_name


def clean_command_name(command_name):
    """
    Cleans Command Name for uncategorised commands
    :param command_name:
    :return:
    """
    final_command_name = command_name.lower().replace(" ", "_").strip()
    final_command_name = re.sub("[\W_-]", "", final_command_name)
    return final_command_name


def print_help():
    """
    Prints help
    :return:
    """
    print("========= creatediscordbot Help =========")
    print("[-] createbot <BotName> : Creates a new Bot with predefined project structure and initial Cog Module")
    print("[-] createcommand <command_name> : Creates a new command in the uncategorised commands folder")
    print("[-] createcog <CogName> [--bare] : Creates a new Cog")
    print("[-] - [--bare] : Does not create modle/controller/converter and test files")
    print("[-] - [--tests] : Does not create test files")
    print("[-] --help : Shows this help")
    print("[-] -h : Shortform for --help")


def save_config(config_object):
    """
    Saves default config file
    :param config_object:
    :return:
    """
    config = configparser.ConfigParser()
    config.read_dict(config_object)

    config_file = os.path.join(os.getcwd(), '.creatediscordbot.conf')
    with open(config_file, 'w') as configfile:
        config.write(configfile)


def read_config():
    """
    Read config file for further adjustments
    :return:
    """
    config = configparser.ConfigParser()
    config_file = os.path.join(os.getcwd(), '.creatediscordbot.conf')
    config.read(config_file)
    return config


def check_if_folder_exists(folder_name):
    """
    Wrapper for ps.path.isdir
    :param folder_name:
    :return:
    """
    return os.path.isdir((folder_name))


def p(msg):
    print("[#] %s " % msg)
    print(Style.RESET_ALL)


def success(msg):
    print(Fore.GREEN + "[=] %s" % msg)
    print(Style.RESET_ALL)


def error(msg):
    print(Fore.RED + "!! %s" % msg)
    print(Style.RESET_ALL)
