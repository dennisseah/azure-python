from azure_python.hosting import container
from azure_python.protocols.i_azure_text2speech_service import IAzureText2SpeechService


def main():
    svc = container[IAzureText2SpeechService]

    svc.synthesize(
        "Hello, this is a sample text to speech conversion using Azure Text to Speech Service.",  # noqa: E501
        "test.wav",
    )


if __name__ == "__main__":
    main()
