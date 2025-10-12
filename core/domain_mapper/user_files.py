from core.dto.user_file_id_pair import UserFileIDPair
from core.db.models.user_files import UserFileModel


class UserFileIdMapper:
    @staticmethod
    def to_model(user_file_id_pair: UserFileIDPair) -> UserFileModel:
        return UserFileModel(
            user_id=user_file_id_pair.user_id,
            file_id=user_file_id_pair.file_id
        )

    @staticmethod
    def to_domain(user_files: UserFileModel) -> UserFileIDPair:
        return UserFileIDPair(
            user_uid=user_files.user_id,
            file_uid=user_files.file_id
        )
