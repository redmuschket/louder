from core.domain.file import File
from core.db.models.file import FileModel


class FileMapper:
    @staticmethod
    def to_model(file: File) -> FileModel:
        return FileModel(
            id=file.uid,
            file_name=file.name,
            file_extension=file.extension,
            is_public=file.is_public,
            file_size=file.size,
            mime_type=file.mime_type,
            created_at=file.created_at,
            updated_at=file.updated_at
        )

    @staticmethod
    def to_domain(model: FileModel) -> File:
        return File(
            name=model.file_name,
            uid=model.id,
            extension=model.file_extension,
            is_public=model.is_public,
            size=model.file_size,
            mime_type=model.mime_type,
            created_at=model.created_at,
            updated_at=model.updated_at
        )