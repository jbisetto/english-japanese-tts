import os
from google.cloud import texttospeech
from google.api_core import exceptions as google_exceptions
from src.speech.tts_service import TTSService
from src.speech.exceptions import TTSConnectionError, TTSInvalidInputError, TTSSynthesisError

class GoogleCloudTTSService(TTSService):
    def __init__(self, config):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.google_cloud_credentials_path
        self.client = texttospeech.TextToSpeechClient()

    def synthesize(self, language: str, text: str, voice_id: str = "en-US-Standard-A") -> bytes:
        """Synthesizes speech from the given text and language using Google Cloud TTS.

        Args:
            language: The language of the text.
            text: The text to synthesize.
            voice_id: The voice ID to use for synthesis (default: en-US-Standard-A).

        Returns:
            The synthesized audio data as bytes.

        Raises:
            TTSConnectionError: If there are connection/authentication issues with Google Cloud TTS.
            TTSInvalidInputError: If the input text or parameters are invalid.
            TTSSynthesisError: If there's an error during speech synthesis.
        """
        if not text.strip():
            raise TTSInvalidInputError("Text cannot be empty")

        try:
            synthesis_input = texttospeech.SynthesisInput(text=text)
            voice = texttospeech.VoiceSelectionParams(
                language_code=language,
                name=voice_id
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000
            )

            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            return response.audio_content
        except google_exceptions.PermissionDenied as e:
            raise TTSConnectionError(f"Google Cloud TTS authentication error: {e}")
        except google_exceptions.InvalidArgument as e:
            raise TTSInvalidInputError(f"Invalid input for Google Cloud TTS: {e}")
        except google_exceptions.GoogleAPIError as e:
            raise TTSSynthesisError(f"Google Cloud TTS synthesis error: {e}")
        except Exception as e:
            raise TTSSynthesisError(f"Unexpected error during Google Cloud TTS synthesis: {e}")
