import logging
import os
import subprocess

from colorama import Fore, Style

DATABASE_URL = "sqlite:///test.db"
SHARED_FOLDER_PATH = "/shared"

logger = logging.getLogger(__name__)

host_process = subprocess.run("hostname", shell=True, capture_output=True, text=True)

if host_process.returncode != 0:
    logger.error(Fore.RED + Style.BRIGHT + "Failed to get hostname" + Style.RESET_ALL)
    exit(1)

HOSTNAME = host_process.stdout.strip()

logger.warning(Fore.YELLOW + Style.BRIGHT + f"Running on {HOSTNAME}" + Style.RESET_ALL)

logger.warning(Fore.YELLOW + Style.BRIGHT + f"DATABASE_URL: {DATABASE_URL}" + Style.RESET_ALL)
logger.warning(Fore.YELLOW + Style.BRIGHT + f"SHARED_FOLDER_PATH: {SHARED_FOLDER_PATH}" + Style.RESET_ALL)

# if DATABASE_URL is None:
#     DATABASE_URL = DEFAULT_DATABASE_URL
#     logger.warning(Fore.RED + Style.BRIGHT + f"DATABASE_URL not set, using default: {DATABASE_URL}" + Style.RESET_ALL)

# if SHARED_FOLDER_PATH is None:
#     SHARED_FOLDER_PATH = DEFAULT_SHARED_FOLDER_PATH
#     logger.warning(Fore.RED + Style.BRIGHT + f"SHARED_FOLDER_PATH not set, using default: {SHARED_FOLDER_PATH}" + Style.RESET_ALL)