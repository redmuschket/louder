from core.config_app import ConfigAPP
from core.logger import Logger
from dotenv import load_dotenv
from pathlib import Path
import argparse
import sys
import os


load_dotenv()

base_dir = Path(__file__).resolve().parent.parent
config = ConfigAPP()

# Creating an argument parser
parser = argparse.ArgumentParser(
    description='My Loader',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
        Examples:
            python main.py                    # Uses development config (default)
            python main.py --env test         # Uses test config
            python main.py --env production   # Uses production config
            python main.py -e dev            # Uses development config
    """
)

# Adding an argument for selecting an environment
parser.add_argument(
    '--env', '-e',
    type=str,
    default='development',
    choices=['development', 'dev', 'test', 'testing', 'production', 'prod'],
    help='Environment configuration (default: development)'
)

parser.add_argument(
    '--config-dir',
    type=str,
    default='configs',
    help='Configuration directory (default: configs)'
)

# Add verbose argument
parser.add_argument(
    '--verbose', '-v',
    action='store_true',
    help='Enable verbose mode'
)

# Parsing arguments
args = parser.parse_args()

# Normalize the name of the environment
env_mapping = {
    'dev': 'development',
    'development': 'development',
    'test': 'test',
    'testing': 'test',
    'prod': 'production',
    'production': 'production'
}

env = env_mapping[args.env]
config_dir = args.config_dir

# Creating the path to the configuration file
config_file = f'{config_dir}/{env}.py'
config_path = base_dir / config_file

# Checking the existence of the file
if not config_path.exists():
    print(f"Error: Config file not found: {config_path}")
    sys.exit(1)

# Load configuration
config.from_pyfile(config_path)

# Adding arguments to the config for use in the application
config.ARGS = args

# Initializing the logger
logger = Logger.init_logger(config)