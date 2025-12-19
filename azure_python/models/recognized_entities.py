from pydantic import BaseModel, field_validator


class RecognizedEntity(BaseModel):
    text: str
    category: str
    subcategory: str | None
    length: int
    offset: int
    confidence_score: float
    sentence: str

    @field_validator("confidence_score")
    @classmethod
    def validate_confidence_score(cls, v):
        if not 0 <= v <= 1:
            raise ValueError("confidence_score must be between 0 and 1")


class RecognizedEntities(BaseModel):
    id: str
    entities: list[RecognizedEntity]
