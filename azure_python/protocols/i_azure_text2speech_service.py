from typing import Literal, Protocol

voices = Literal[
    "en-GB-ThomasNeural",  # English (United Kingdom)
    "en-SG-WayneNeural",  # English (Singapore)
    "en-US-MonicaNeural",  # English (USA)
    "en-US-EricNeural",  # English (USA)
    "en-IN-NeerjaNeural",  # Engish (India)
]


class IAzureText2SpeechService(Protocol):
    def synthesize(
        self, text: str, output_file: str, voice: voices = "en-US-MonicaNeural"
    ) -> bool:
        """Synthesize speech from text and save to output file.

        :param text: The text to be synthesized.
        :param output_file: The path to the output audio file.
        :param voice: The voice to be used for synthesis.
        :return: True if synthesis was successful, False otherwise.
        """
        ...
