from core.domain.file import File
from core.db.models.file import FileModel
from app.http.response_models.file import FilesResponse, FileFieldsResponse
from core.data_mapper.mapper import StaticMapper


class FilesMapper(StaticMapper[list[File], list[FileModel], list[FilesResponse]]):

    @staticmethod
    def to_model(files: list[File]) -> list[FileModel]:
        """Convert system files to database models"""
        return [
            FileModel(
                id=file.uid,
                file_name=file.name,
                file_extension=file.extension or "",
                is_public=file.is_public or False,
                file_size=file.size or 0,
                mime_type=file.mime_type or "",
                created_at=file.created_at,
                updated_at=file.updated_at
            )
            for file in files
        ]

    @staticmethod
    def to_domain(models: list[FileModel]) -> list[File]:
        """Convert database models to system files"""
        return [
            File(
                uid=model.id,
                name=model.file_name,
                extension=model.file_extension,
                is_public=model.is_public,
                size=model.file_size,
                mime_type=model.mime_type,
                created_at=model.created_at,
                updated_at=model.updated_at
            )
            for model in models
        ]

    @staticmethod
    def to_pydantic(files: list[File]) -> FilesResponse:
        """Convert system files to Pydantic responses"""
        return FilesResponse(
            files={
                file.uid: FileFieldsResponse(
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
                for file in files
            }
        )
