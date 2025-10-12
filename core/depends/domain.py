from typing import Annotated, Optional
from fastapi import Depends, Header, Path, HTTPException
from uuid import UUID
from uuid6 import uuid7
from core.dto.user_file_id_pair import UserFileIDPair


async def get_user_file_id_pair(
        x_user_uid: Annotated[str, Header(alias="X-User-Id")],
        file_uid: Annotated[Optional[str], Path()] = None,
) -> UserFileIDPair:
    try:
        user_uuid = UUID(x_user_uid)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    if file_uid is None:
        file_uuid = uuid7()
    else:
        try:
            file_uuid = UUID(file_uid)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid file ID format")

    return UserFileIDPair(user_uid=user_uuid, file_uid=file_uuid)