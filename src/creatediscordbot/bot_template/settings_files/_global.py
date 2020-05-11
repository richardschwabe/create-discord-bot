import os
import yaml
import logging
import logging.config
from pathlib import Path

global_settings_file_path = Path(__file__)

# Set DEBUG
DEBUG = bool(os.getenv("DEBUG", False))

# Define Folder where settings are located
SETTINGS_DIR = global_settings_file_path.parent

# Define project root folder to main.py
ROOT_DIR = SETTINGS_DIR.parent

# Define folder where data files are located
DATA_DIR = ROOT_DIR / 'data'

# Define where folder where Cogs are located
COGS_FOLDER = ROOT_DIR / 'cogs'

# Define where folder for logs is located
LOGS_FOLDER = ROOT_DIR.parent / 'logs'

# Define where uncategorised commands are located
UNCATEGORISED_COMMANDS_DIR = ROOT_DIR / 'uncategorised_commands'

# Discord Conf
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", None)

DISCORD_COMMAND_PREFIX = "!"

# Database Configuration
DB_HOST_NAME = os.getenv("DB_HOST_NAME")
DB_DATABASE_NAME = os.getenv("DB_DATABASE_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Logging
logfile = "logger.prod.yml"
if DEBUG:
    logfile = "logger.yml"

with open(ROOT_DIR / logfile, "rt") as file:
    config = yaml.safe_load(file.read())
    logging.config.dictConfig(config)
