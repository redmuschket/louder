from core.config_app import ConfigAPP
from core.logger import Logger
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

base_dir = Path(__file__).resolve().parent.parent

config = ConfigAPP()
config.from_pyfile(base_dir / 'configs/development.py')

# logger
logger = Logger.init_logger(config)