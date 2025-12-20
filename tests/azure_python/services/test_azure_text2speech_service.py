from pathlib import Path
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from azure_python.services.azure_text2speech_service import (
    AzureText2SpeechService,
    AzureText2SpeechServiceEnv,
)


@pytest.mark.parametrize("error", [True, False])
def test_synthesize(error: bool, mocker: MockerFixture, tmpdir: Path) -> None:
    mock_speech = mocker.patch("azure_python.services.azure_text2speech_service.speech")
    mock_speech.SpeechSynthesizer.return_value.speak_text_async.return_value.get.return_value = MagicMock(  # noqa: E501
        reason=mock_speech.ResultReason.SynthesizingAudioCompleted
        if not error
        else mock_speech.ResultReason.Canceled,  # noqa: E501
        audio_data=b"fake_audio_data",
    )
    svc = AzureText2SpeechService(
        env=AzureText2SpeechServiceEnv(
            azure_speech_key="fake_key", azure_speech_region="fake_region"
        ),
        logger=MagicMock(),
    )

    output_file = tmpdir / "output_test.mp3"
    status = svc.synthesize("This is a test.", str(output_file))

    if error:
        assert not status
        assert not output_file.exists()
    else:
        assert status
        assert output_file.exists()
        with open(output_file, "rb") as audio_file:
            audio_data = audio_file.read()
            assert audio_data == b"fake_audio_data"
