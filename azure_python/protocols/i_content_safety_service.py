from typing import Protocol


class IContentSafetyService(Protocol):
    async def analyze_text(self, text: str) -> list[dict]:
        """Analyze the given text for content safety.

        :param text: The text to be analyzed.
        :return: A list of dictionaries containing the analysis results.
        """
        ...
