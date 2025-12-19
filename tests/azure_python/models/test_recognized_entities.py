from unittest.mock import MagicMock

import pytest

from azure_python.models.recognized_entities import (
    RecognizedEntities,
    RecognizedEntity,
)


def test_entity_invalid_confidence_scores():
    with pytest.raises(ValueError, match="confidence_score must be between 0 and 1"):
        RecognizedEntity(
            text="text",
            category="category",
            subcategory="subcategory",
            length=1,
            offset=0,
            confidence_score=10.0,
            sentence="sentence",
        )


def test_entitities_init():
    entities = RecognizedEntities(
        id="0",
        entities=[MagicMock(spec=RecognizedEntity), MagicMock(spec=RecognizedEntity)],
    )
    assert entities.id == "0"
    assert len(entities.entities) == 2
