from app.response.registration import UserResponse
from typing import NamedTuple
from core.dto import TokenPair


class RegistrationPair(NamedTuple):
    token: TokenPair
    new_user: UserResponse
