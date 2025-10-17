import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional
from core.config_app import ConfigAPP


class Logger:
    _instance: Optional['Logger'] = None
    _handlers_initialized: bool = False

    def __init__(self, configAPP: ConfigAPP):
        self.config = configAPP
        self._setup_logging()

    def _setup_logging(self):
        if Logger._handlers_initialized:
            return

        log_dir = Path(self.config.get('LOG_DIR', 'logs'))
        log_dir.mkdir(exist_ok=True, parents=True)

        formatter = logging.Formatter(
            self.config.get(
                'LOG_FORMAT',
                '%(asctime)s - %(name)s - %(levelname)s - '
                '[%(filename)s:%(lineno)d - %(funcName)s()] - %(message)s'
            )
        )

        log_level = logging.DEBUG if self.config.get('DEBUG', False) else logging.INFO
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)

        def make_handler(filename: str, level: int) -> RotatingFileHandler:
            handler = RotatingFileHandler(
                filename=log_dir / filename,
                maxBytes=self.config.get('LOG_MAX_BYTES', 10 * 1024 * 1024),
                backupCount=self.config.get('LOG_BACKUP_COUNT', 5),
                encoding=self.config.get('LOG_ENCODING', 'utf-8')
            )
            handler.setFormatter(formatter)
            handler.setLevel(level)
            return handler

        class InfoFilter(logging.Filter):
            def filter(self, record):
                return logging.INFO <= record.levelno < logging.ERROR

        info_handler = make_handler('info.log', logging.INFO)
        info_handler.addFilter(InfoFilter())
        root_logger.addHandler(info_handler)

        error_handler = make_handler('errors.log', logging.ERROR)
        root_logger.addHandler(error_handler)

        if self.config.get('DEBUG', False):
            debug_handler = make_handler('debug.log', logging.DEBUG)
            root_logger.addHandler(debug_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(log_level)
        root_logger.addHandler(console_handler)

        Logger._handlers_initialized = True

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        if Logger._instance is None:
            raise RuntimeError("Logger is not initialized. Call Logger.init_logger(config) first.")
        return logging.getLogger(name)

    @classmethod
    def init_logger(cls, configAPP: ConfigAPP) -> 'Logger':
        if not cls._instance:
            cls._instance = cls(configAPP)
        return cls._instance
