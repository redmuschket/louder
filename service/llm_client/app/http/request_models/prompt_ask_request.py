from pydantic import BaseModel, field_validator
from core.enum.purpose_provider import AIProviderPurpose


class AskRequest(BaseModel):
    user_uuid: str
    prompt: str
    purpose: AIProviderPurpose

    @field_validator('purpose', mode='before')
    @classmethod
    def validate_purpose(cls, v):
        if isinstance(v, AIProviderPurpose):
            return v
        try:
            return AIProviderPurpose(v.lower())
        except ValueError:
            allowed = [e.value for e in AIProviderPurpose]
            raise ValueError(f"Allowed purposes: {allowed}")