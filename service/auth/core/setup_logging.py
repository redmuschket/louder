import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional, Dict
from core.config_app import ConfigAPP

class Logger:
    _instance: Optional['Logger'] = None

    def __init__(self, configAPP: ConfigAPP):
        self.config = configAPP
        self._setup_logging()
        self.logger = logging.getLogger('app')  # Main application logger

    def _setup_logging(self):
        log_dir = Path(self.config.get('LOG_DIR', 'logs'))
        log_dir.mkdir(exist_ok=True)

        # Common formatter for all handlers
        formatter = logging.Formatter(
            self.config.get('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )

        # --- System logs (aiogram) ---
        system_handler = RotatingFileHandler(
            filename=log_dir / 'system.log',
            maxBytes=self.config.get('LOG_MAX_BYTES', 10 * 1024 * 1024),
            backupCount=self.config.get('LOG_BACKUP_COUNT', 5),
            encoding=self.config.get('LOG_ENCODING', 'utf-8')
        )
        system_handler.setFormatter(formatter)
        system_handler.setLevel(logging.WARNING)  # Only warnings and errors

        system_logger = logging.getLogger('aiogram')
        system_logger.addHandler(system_handler)
        system_logger.propagate = False  # Prevent duplicate logs in root logger

        # --- Application logs ---
        user_logger = logging.getLogger('app')
        user_logger.setLevel(logging.DEBUG)  # Capture all levels, filtering happens in handlers

        # ConfigAPPure different log files for different levels
        handlers = [
            ('info.log', logging.INFO),
            ('errors.log', logging.ERROR)
        ]

        # Add debug log file only in debug mode
        if self.config.get('DEBUG', False):
            handlers.append(('debug.log', logging.DEBUG))

        # Create file handlers for each log level
        for filename, level in handlers:
            handler = RotatingFileHandler(
                filename=log_dir / filename,
                maxBytes=self.config.get('LOG_MAX_BYTES', 10 * 1024 * 1024),
                backupCount=self.config.get('LOG_BACKUP_COUNT', 5),
                encoding=self.config.get('LOG_ENCODING', 'utf-8')
            )
            handler.setFormatter(formatter)
            handler.setLevel(level)
            user_logger.addHandler(handler)

        # Console output ConfigAPPuration
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_level = logging.DEBUG if self.config.get('DEBUG', False) else logging.INFO
        console_handler.setLevel(console_level)
        user_logger.addHandler(console_handler)

        # Disable unnecessary system logs
        logging.getLogger('asyncio').setLevel(logging.WARNING)

    @classmethod
    def init_logger(cls, configAPP: ConfigAPP) -> 'Logger':
        if not cls._instance:
            cls._instance = cls(configAPP)
        return cls._instance

# Global access point
logger: Optional[logging.Logger] = None