import os
from pathlib import Path
import yaml
from sqlalchemy.pool import NullPool

with open('paths_config.yaml', 'r', encoding='utf-8') as f:
    paths_config = yaml.safe_load(f)

# SYSTEM
USER_FILE_UUID_RESTRICTION = {7} # version
BASE_DIR = Path(__file__).resolve().parent.parent
PATH_YAML_FILE = os.path.join(BASE_DIR, 'paths_config.yaml')

#STORAGE
STORAGE_DIR = Path(paths_config['storage']['base_path'])
STORAGE_USER_DATA_DIR = STORAGE_DIR / paths_config['storage']['user_data_dir']
STORAGE_PROMPTS_DIR = STORAGE_DIR / paths_config['storage']['prompts_dir']
USER_FILE_PATH = paths_config['templates']['user_file']

# SERVICE URLS
USER_SERVICE_URL = os.getenv('USER_SERVICE_URL')
PARSER_SERVICE_URL = os.getenv('PARSER_SERVICE_URL')
LLMCLIENT_SERVICE_URL = os.getenv('LLMCLIENT_SERVICE_URL')

# LOGS
LOG_DIR = Path(paths_config['system']['logs_dir'])
LOG_FILE_SYSTEM = LOG_DIR / "system.log"
LOG_FILE_USER = LOG_DIR / "user_actions.log"
LOG_MAX_BYTES = 10 * 1024 * 1024  # 10 MB
LOG_BACKUP_COUNT = 5
LOG_ENCODING = 'utf-8'

# LOG FORMATS
LOG_SYSTEM_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_USER_FORMAT = '%(asctime)s - %(message)s'

# LOGGING LEVELS
LOG_FILE_LEVEL = 'INFO'
LOG_CONSOLE_LEVEL = 'DEBUG'
LOG_ROOT_LEVEL = 'DEBUG'
LOG_WERKZEUG_LEVEL = 'INFO'

DEBUG = True

# DB
DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_ECHO = os.getenv("DATABASE_ECHO")
DATABASE_POOL_SIZE = int(os.getenv("DATABASE_POOL_SIZE"))
DATABASE_MAX_OVERFLOW = int(os.getenv("DATABASE_MAX_OVERFLOW"))
DATABASE_PRE_PING = os.getenv("DATABASE_PRE_PING")
DATABASE_POOL_RECYCLE = int(os.getenv("DATABASE_POOL_RECYCLE"))

pool_class = os.getenv("DATABASE_POOL_CLASS", "NullPool")
if pool_class == "NullPool":
    DATABASE_POOL_CLASS = NullPool
else:
    DATABASE_POOL_CLASS = None

DATABASE_EXPIRE_ON_COMMIT = os.getenv("DATABASE_EXPIRE_ON_COMMIT")
DATABASE_AUTOCOMMIT = os.getenv("DATABASE_AUTOCOMMIT")
DATABASE_AUTOFLUSH = os.getenv("DATABASE_AUTOFLUSH")
DATABASE_FUTURE = os.getenv("DATABASE_FUTURE")