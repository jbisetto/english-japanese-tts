import os
import boto3
from src.speech.tts_service import TTSService

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
        """
        try:
            response = self.polly_client.synthesize_speech(
                Text=text,
                OutputFormat="pcm",
                VoiceId=voice_id,
                SampleRate="16000"
            )
            audio_stream = response["AudioStream"].read()
            return audio_stream
        except Exception as e:
            print(f"Error synthesizing speech: {e}")
            return b""
