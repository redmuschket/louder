from fastapi import status
from typing import Dict

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


class FileCreationResponses(BaseAPIResponse):
    """Responses for file creation operations"""

    @classmethod
    def get_responses(cls) -> Dict[int, Dict]:
        return {
            **cls.error(
                status.HTTP_400_BAD_REQUEST,
                "Invalid user ID format",
                "Invalid file ID format"
            ),
            **cls.error(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "File creation failed",
                "Failed to create file"
            ),
            **cls.error(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Internal server error",
                "Internal server error during file create"
            ),
            **cls.error(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                "Validation error",
                "Invalid data format"
            )
        }

    @staticmethod
    def success_example():
        return {
            "application/json": {
                "example": {
                    "file_uid": "123e4567-e89b-12d3-a456-426614174000"
                }
            }
        }