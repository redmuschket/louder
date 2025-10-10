from core.logger import Logger
from typing import Dict
import aiofiles
import json
import os

logger = Logger.get_logger(__name__)

class DBService:

    @staticmethod
    async def get_from_db_json(storage_path) -> Dict:
        print(storage_path)
        logger.debug("Start reading json analog from DB")
        if not storage_path.exists() or os.path.getsize(storage_path) == 0:
            DBService.check_and_create_storage(storage_path)
            return {}
        try:
            async with aiofiles.open(storage_path, 'r', encoding='utf-8') as f:
                content = await f.read()
                try:
                    data = json.loads(content)
                    if isinstance(data, dict):
                        logger.debug("Successfully read json from DB")
                        return data
                    else:
                        logger.warning("Json file does not contain a dictionary")
                        return {}
                except json.JSONDecodeError:
                    logger.error("Failed to decode JSON")
                    return {}
        except Exception as e:
            logger.error(f"Error reading json file: {e}")
            return {}

    @staticmethod
    async def get_from_db_text(storage_path) -> str:
        logger.debug("Start reading text from DB")
        if not storage_path.exists() or os.path.getsize(storage_path) == 0:
            DBService.check_and_create_storage(storage_path)
            return ""
        try:
            async with aiofiles.open(storage_path, 'r', encoding='utf-8') as f:
                content = await f.read()
                logger.debug("Successfully read text from DB")
                return content
        except Exception as e:
            logger.error(f"Error reading text file: {e}")
            return ""

    @staticmethod
    async def save_in_db_json(storage_path, data) -> bool:
        logger.debug("The beginning of saving json to the database")
        DBService.check_and_create_storage(storage_path)
        try:
            json_data = json.dumps(data, ensure_ascii=False, indent=4)
            async with aiofiles.open(storage_path, 'w', encoding='utf-8') as f:
                await f.write(json_data)
            logger.debug("Saving the analog in the database was successful")
            return True
        except Exception as e:
            logger.error(f"Error saving file json: {e}")
            return False

    @staticmethod
    async def save_in_db_text(storage_path, data) -> bool:
        logger.debug("The beginning of saving text to the database")
        if not DBService.check_and_create_storage(storage_path):
            return False
        try:
            async with aiofiles.open(storage_path, 'w', encoding='utf-8') as f:
                await f.write(data)
            logger.debug("Saving in the database was successful text")
            return True
        except Exception as e:
            logger.error(f"Error saving file text: {e}")
            return False

    @staticmethod
    def check_and_create_storage(path) -> bool:
        logger.debug("We check the availability of the database or create")
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists():
                path.write_text("{}", encoding="utf-8")
        except PermissionError:
            logger.error(
                "Couldn't create a folder to save the parsing results: not have the rights to create a directory.")
            return False
        except FileNotFoundError:
            logger.error("Uncorrected path for creating a folder for storing parsing results")
            return False
        except OSError as e:
            logger.error(f"Unknown error when creating a folder for storing parsing results: {e}")
            return False
        except Exception as e:
            logger.error(e)
            return False
        logger.debug("Verification or creation was successful")
        return True