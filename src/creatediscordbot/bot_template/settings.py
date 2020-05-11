import os
from pathlib import Path
import logging

DEBUG = os.getenv("DEBUG", False)
DOCKER_DEBUG = os.getenv("DOCKER_DEBUG", False)

if DEBUG and not DOCKER_DEBUG:
    # use dotenv to load .env.debug file
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / ".env.debug"
    load_dotenv(dotenv_path=env_path)

    # import everything from development settings
    from settings_files.development import *
    # if everything is correctly setup you should be notified that you are in debug, via the logger
    logger = logging.getLogger(__name__)
    logger.debug("We are in Debug")
elif DOCKER_DEBUG:
    # import everything from development settings
    from settings_files.development import *
    # if everything is correctly setup you should be notified that you are in debug, via the logger
    logger = logging.getLogger(__name__)
    logger.debug("We are in Docker Debug")
else:
    from settings_files.production import *
