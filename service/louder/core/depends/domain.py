from typing import Annotated, Optional
from fastapi import Depends, Header, Path, HTTPException
from uuid6 import uuid7, UUID
from core.dto.user_file_id_pair import UserFileIDPair


async def get_user_file_id_pair(
        x_user_uid: Annotated[str, Header(alias="X-User-Id")],
        file_uid: Annotated[str, Path()],
) -> UserFileIDPair:
    try:
        user_uuid = UUID(x_user_uid)

        if file_uid is None:
            file_uuid = uuid7()
        else:
            file_uuid = UUID(file_uid)

        return UserFileIDPair(user_uid=user_uuid, file_uid=file_uuid)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid UUID format: {str(e)}")