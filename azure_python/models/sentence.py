from pydantic import BaseModel, field_validator


class Sentence(BaseModel):
    content: str
    start: int

    @field_validator("start")
    @classmethod
    def validate_start(cls, v: int) -> int:
        if v < 0:
            raise ValueError("start must be greater than or equal to 0")
        return v

    @staticmethod
    def includes(sentences: list["Sentence"], start: int) -> str:
        for sentence in sentences:
            if start >= sentence.start and start <= sentence.start + len(
                sentence.content
            ):
                return sentence.content

        raise RuntimeError(f"Sentence not found with start index: {start}")
