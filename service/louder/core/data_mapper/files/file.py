from core.domain.file import File
from core.db.models.file import FileModel
from app.http.response_models.file import FileFieldsResponse
from core.data_mapper.mapper import StaticMapper
from uuid6 import UUID


class FileMapper(StaticMapper[File, FileModel, FileFieldsResponse]):

    @staticmethod
    def to_model(file: File) -> FileModel:
        """Convert to db model"""
        return FileModel(
            id=str(file.uid),
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
        """Convert to system model"""
        return File(
            name=model.file_name,
            uid=UUID(model.id),
            extension=model.file_extension,
            is_public=model.is_public,
            size=model.file_size,
            mime_type=model.mime_type,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    @staticmethod
    def to_pydantic(file: File) -> FileFieldsResponse:
        """Convert to Pydantic model"""
        return FileFieldsResponse(
            uid=file.uid,
            name=file.name,
            extension=file.extension,
            is_public=file.is_public,
            size=file.size,
            mime_type=file.mime_type,
            created_at=file.created_at,
            updated_at=file.updated_at,
            filename=file.filename,
            storage_filename=file.storage_filename,
            size_in_mb=file.size_in_mb,
            size_in_kb=file.size_in_kb
        )