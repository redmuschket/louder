from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler
import uuid6


class UUID6(uuid6.UUID):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema()
        )

    @classmethod
    def validate(cls, value: str):
        try:
            return cls(value)
        except Exception as e:
            raise ValueError(f'Invalid UUID6 string: {value}') from e