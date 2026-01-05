from dataclasses import dataclass
from logging import Logger

from azure.cognitiveservices import speech
from lagom.environment import Env

from azure_python.protocols.i_azure_text2speech_service import (
    IAzureText2SpeechService,
    voices,
)


@dataclass
class SynthesisResult:
    audio_data: bytes
    reason: str


class AzureText2SpeechServiceEnv(Env):
    azure_speech_key: str
    azure_speech_region: str


@dataclass
class AzureText2SpeechService(IAzureText2SpeechService):
    env: AzureText2SpeechServiceEnv
    logger: Logger

    def synthesize(
        self, text: str, output_file: str, voice: voices = "en-US-MonicaNeural"
    ) -> bool:
        self.logger.debug(
            f"[BEGIN] synthesize text to {output_file} using voice {voice}"
        )
        speech_config = speech.SpeechConfig(
            subscription=self.env.azure_speech_key, region=self.env.azure_speech_region
        )
        speech_config.set_speech_synthesis_output_format(
            speech.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
        )
        speech_config.speech_synthesis_voice_name = voice

        synthesizer = speech.SpeechSynthesizer(speech_config=speech_config)

        result: SynthesisResult = synthesizer.speak_text_async(text).get()  # type: ignore

        if result.reason == speech.ResultReason.SynthesizingAudioCompleted:
            with open(output_file, "wb") as audio_file:
                audio_file.write(result.audio_data)
            self.logger.debug(
                f"[COMPLETED] Speech synthesized and saved to {output_file}"
            )
            return True

        self.logger.error(f"[ERROR] Speech synthesis failed: {result.reason}")
        return False
