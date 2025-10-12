from typing import Annotated
from fastapi import Depends
from uuid6 import uuid7
from sqlalchemy.orm import Session

from app.services.file import FileService
from core.dto.user_file_id_pair import UserFileIDPair
from core.db.db import get_db
from core.manager_domain.user import UserManagerDomain
from core.manager_domain.user_file import UserFilesManagerDomain
from core.depends.domain import get_user_file_id_pair
from app.services.path_master import PathMaster


SessionDep = Annotated[Session, Depends(get_db)]
UserFileIDPairDep = Annotated[UserFileIDPair, Depends(get_user_file_id_pair)]


async def get_path_master(user_file_id_pair: UserFileIDPairDep):
    user = UserManagerDomain().get(user_file_id_pair.user_uid)
    file_manager = UserFilesManagerDomain().get(user_file_id_pair.user_uid)
    file = file_manager.get(user_file_id_pair.file_uid)
    FileService.file_registration_in_domain_system(user, file)
    return PathMaster(user_file_id_pair)


PathMasterDep = Annotated[PathMaster, Depends(get_path_master)]


def get_file_service(
        db: SessionDep,
        path_master: PathMasterDep,
        user_file_id_pair: UserFileIDPairDep) -> FileService:
    return FileService(db=db, path_master=path_master, user_file_id_pair=user_file_id_pair)
