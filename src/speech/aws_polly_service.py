import boto3
from botocore.exceptions import BotoCoreError, ClientError
from src.speech.tts_service import TTSService
from src.speech.exceptions import TTSConnectionError, TTSInvalidInputError, TTSSynthesisError

class AWSPollyService(TTSService):
    def __init__(self, config):
        self.polly_client = boto3.client(
            "polly",
            region_name=config.aws_region_name,
            aws_access_key_id=config.aws_access_key_id,
            aws_secret_access_key=config.aws_secret_access_key
        )

    def synthesize(self, language: str, text: str, voice_id: str = "Joanna") -> bytes:
        """Synthesizes speech from the given text and language using AWS Polly.

        Args:
            language: The language of the text.
            text: The text to synthesize.
            voice_id: The voice ID to use for synthesis (default: Joanna).

        Returns:
            The synthesized audio data as bytes.

        Raises:
            TTSConnectionError: If there are connection/authentication issues with AWS Polly.
            TTSInvalidInputError: If the input text or parameters are invalid.
            TTSSynthesisError: If there's an error during speech synthesis.
        """
        if not text.strip():
            raise TTSInvalidInputError("Text cannot be empty")

        try:
            response = self.polly_client.synthesize_speech(
                Text=text,
                OutputFormat="pcm",
                VoiceId=voice_id,
                SampleRate="16000"
            )
            audio_stream = response["AudioStream"].read()
            return audio_stream
        except (BotoCoreError, ClientError) as e:
            if "AccessDenied" in str(e) or "UnrecognizedClientException" in str(e):
                raise TTSConnectionError(f"AWS Polly authentication error: {e}")
            elif "ValidationException" in str(e) or "InvalidParameterValue" in str(e):
                raise TTSInvalidInputError(f"Invalid input for AWS Polly: {e}")
            else:
                raise TTSSynthesisError(f"AWS Polly synthesis error: {e}")
        except Exception as e:
            raise TTSSynthesisError(f"Unexpected error during AWS Polly synthesis: {e}")
