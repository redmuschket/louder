from typing import Dict, Any
from fastapi import status


class BaseAPIResponse:
    """Base class for API responses"""

    @staticmethod
    def error(status_code: int, description: str, detail: str):
        return {
            status_code: {
                "description": description,
                "content": {
                    "application/json": {
                        "example": {"detail": detail}
                    }
                }
            }
        }


class FileResponses(BaseAPIResponse):
    """Responses for file operations"""

    @classmethod
    def get_responses(cls) -> Dict[int, Dict]:
        return {
            **cls.error(
                status.HTTP_400_BAD_REQUEST,
                "Invalid user ID format",
                "Invalid user ID format. Must be a valid UUID."
            ),
            **cls.error(
                status.HTTP_404_NOT_FOUND,
                "Files not found",
                "Files not found or access denied"
            ),
            **cls.error(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                "Validation error",
                "Invalid data format"
            ),
            **cls.error(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Internal server error",
                "Internal server error"
            ),
            **cls.error(
                status.HTTP_503_SERVICE_UNAVAILABLE,
                "Service unavailable",
                "Temporary service unavailable. Please try again later."
            )
        }

    @staticmethod
    def success_example():
        return {
            "application/json": {
                "example": {
                    "files": {
                        "123e4567-e89b-12d3-a456-426614174000": {
                            "uid": "123e4567-e89b-12d3-a456-426614174000",
                            "name": "Отчёт",
                            "extension": ".pdf",
                            "is_public": False,
                            "size": 1024,
                            "mime_type": "application/pdf",
                            "created_at": "2023-10-01T12:00:00Z",
                            "updated_at": "2023-10-01T12:00:00Z",
                            "filename": "document.pdf",
                            "storage_filename": "123e4567-e89b-12d3-a456-426614174000.pdf",
                            "size_in_mb": 0.001,
                            "size_in_kb": 1.0
                        },
                        "112e4567-e23b-12d3-a456-426614174000": {
                            "uid": "123e4567-e89b-12d3-a456-426614174000",
                            "name": "Моя картинка",
                            "extension": ".png",
                            "is_public": False,
                            "size": 3024,
                            "mime_type": "image/png",
                            "created_at": "2023-10-01T12:00:00Z",
                            "updated_at": "2023-10-01T12:00:00Z",
                            "filename": "img.png",
                            "storage_filename": "112e4567-e23b-12d3-a456-426614174000.pdf",
                            "size_in_mb": 0.001,
                            "size_in_kb": 1.0
                        }
                    }
                }
            }
        }