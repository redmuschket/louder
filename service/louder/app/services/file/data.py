from core.domain.file import File
from core.dto.user_file_id_pair import UserFileIDPair
from core.logger import Logger
from core.manager_domain.user_file import UserFilesManagerDomain
from core.manager_domain.user import UserManagerDomain
from core.domain.user import User

from uuid6 import uuid7, UUID

logger = Logger.get_logger(__name__)


class FileDataService:

    @staticmethod
    def create_base_file_domain(file_name: str) -> File:
        """
        Creates a domain object File with validation

        Args:
           file_name: File Name

        Returns:
           File: The created domain object

        Raises:
           ValueError: If the parameters are invalid
        :param file_name
        """
        try:
            return File(name=file_name, uid=uuid7())
        except Exception as e:
            logger.error(f"Error creating file '{file_name}': {e}")
            raise

    @staticmethod
    def file_registration_in_domain_system(user: User, file: File) -> None:
        """
        Registers a file in the domain system for the specified user.

        This method adds the user to the domain manager, creates a user files manager,
        and registers the file with the appropriate file manager.

        Args:
            user (User): The user domain object to register
            file (File): The file domain object to register

        Note:
            This operation is performed after successful database persistence.
        """
        logger.debug(f"Registration in domain system{str(user.uid):8}")
        UserManagerDomain().add(user)
        UserFilesManagerDomain().add(user_uid=user.uid)
        file_manager = UserFilesManagerDomain().get(user_uid=user.uid)
        file_manager.add(file)

    @staticmethod
    def create_base_user_files_dto(user_uid: UUID, file_uid: UUID) -> UserFileIDPair:
        """
        Creates a domain object UserFileIDPair with validation

        Args:
           user_file_id_pair: File Name

        Returns:
           File: The created domain object

        Raises:
           ValueError: If the parameters are invalid
           :param file_uid:
           :param user_uid:
        """
        try:
            return UserFileIDPair(
                user_uid=user_uid,
                file_uid=file_uid
            )
        except Exception as e:
            logger.error(f"Error creating user_file_id_pair '{str(user_uid)[:8]}', '{str(file_uid)[:8]}': {e}")
            raise
