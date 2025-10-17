from app.response.registration import UserResponse
from typing import NamedTuple
from app.dto.token_pair import TokenPair


class RegistrationPair(NamedTuple):
    token: TokenPair
    new_user: UserResponse
