import os
from string import Template


def replace_cog_placeholder(cog_name, cog_template_file_name=None, cog_file=None):
    """
    Replaces Placeholders in Cog Template file with actual Cog Class Name, based on Foldername
    :param cog_name:
    :param cog_file:
    :return:
    """
    # check we have both paths available
    if cog_file is None or cog_template_file_name is None:
        return False

    # replacement dictionary
    replacements = {
        "REPLACE_COG_CLASS_NAME": cog_name.capitalize(),
        "REPLACE_METHOD_NAME": f"{cog_name}_foo",
        "REPLACE_CONTROLLER_NAME": f'{cog_name.capitalize()}Controller'
    }

    return create_replace_delete(replacements, cog_template_file_name, cog_file)


def replace_controller_placeholder(cog_name, controller_template_file_name=None, controller_file=None):
    """
    Replaces placeholders in controller with cog_name, for instance admin cog => AdminController

    :param cog_name:
    :param controller_template_file_name:
    :param controller_file:
    :return:
    """
    # check we have both paths available
    if controller_file is None or controller_template_file_name is None:
        return False

    # replacement dictionary
    replacements = {
        "REPLACE_CONTROLLER_CLASS_NAME": f'{cog_name.capitalize()}Controller',
    }

    return create_replace_delete(replacements, controller_template_file_name, controller_file)


def replace_uncategorised_command_placeholder(command_name, command_template_file_name=None, command_file=None):
    """
    Replaces command name for uncategorised commands that are dynamically loaded

    :param command_name:
    :param command_template_file_name:
    :param command_file:
    :return:
    """
    # check we have both paths available
    if command_file is None or command_template_file_name is None or command_name == "":
        return False

    # replacement dictionary
    replacements = {
        "REPLACE_COMMAND_NAME": command_name,
    }

    return create_replace_delete(replacements, command_template_file_name, command_file)


def replace_docker_compose_placeholder(bot_folder_name, template_file_name=None, final_file=None):
    # check we have both paths available
    if final_file is None or template_file_name is None or bot_folder_name == "":
        return False

    bot_name = os.path.basename(bot_folder_name)
    # replacement dictionary
    replacements = {
        "REPLACE_BOT_NAME": bot_name,
    }

    return create_replace_delete(replacements, template_file_name, final_file)


def replace_dockerfile_placeholder(bot_folder_name, template_file_name=None, final_file=None):
    # check we have both paths available
    if final_file is None or template_file_name is None or bot_folder_name == "":
        return False

    bot_name = os.path.basename(bot_folder_name)
    # replacement dictionary
    replacements = {
        "REPLACE_BOT_FOLDER_NAME": bot_name,
    }

    return create_replace_delete(replacements, template_file_name, final_file)


def create_replace_delete(replacements=None, template_file_name=None, final_file_name=None):
    """
    Internal method used by other specific methods to keep code simpler
    :param replacements:
    :param template_file_name:
    :param final_file_name:
    :return:
    """
    if not replacements or not template_file_name or not final_file_name:
        # Todo provide proper message to developer / user
        return False

    try:
        # setup template file and substitude
        filein = open(template_file_name)

        src = Template(filein.read())

        substituted = src.substitute(replacements)

        # Save new file
        with open(final_file_name, 'wt') as fout:
            fout.write(substituted)

    except Exception as e:
        print(e)
        return False

    return True
