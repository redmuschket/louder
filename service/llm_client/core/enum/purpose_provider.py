from enum import Enum


class AIProviderPurpose(Enum):
    ATTRIBUTE_GENERATION = "attribute_generation"
    ATTRIBUTE_MATCHER = "attribute_matcher"
    CHECKING_ATTRIBUTE = "checking_attribute"
