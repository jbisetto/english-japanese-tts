import os
import boto3
from src.speech.tts_service import TTSService

class AWSPollyService(TTSService):
    def __init__(self):
        self.polly_client = boto3.client(
            "polly",
            region_name=os.environ.get("AWS_REGION_NAME"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
        )

    def synthesize(self, language: str, text: str, voice_id: str = "Joanna") -> bytes:
        """Synthesizes speech from the given text and language using AWS Polly.

        Args:
            language: The language of the text.
            text: The text to synthesize.
            voice_id: The voice ID to use for synthesis (default: Joanna).

        Returns:
            The synthesized audio data as bytes.
        """
        try:
            response = self.polly_client.synthesize_speech(
                Text=text,
                OutputFormat="pcm",
                VoiceId=voice_id
            )
            audio_stream = response["AudioStream"].read()
            return audio_stream
        except Exception as e:
            print(f"Error synthesizing speech: {e}")
            return b""
