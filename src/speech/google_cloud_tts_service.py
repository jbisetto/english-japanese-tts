import os
from google.cloud import texttospeech

class GoogleCloudTTSService:
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()

    def synthesize(self, language: str, text: str, voice_id: str = None) -> bytes:
        """Synthesizes speech from the given text and language using Google Cloud TTS.

        Args:
            language: The language of the text ('en' or 'ja').
            text: The text to synthesize.
            voice_id: The voice ID to use for synthesis.

        Returns:
            The synthesized audio data as bytes.
        """
        try:
            # Set the text input to be synthesized
            synthesis_input = texttospeech.SynthesisInput(text=text)

            # Build the voice request
            language_code = "en-US" if language == "en" else "ja-JP"
            voice = texttospeech.VoiceSelectionParams(
                language_code=language_code,
                name=voice_id if voice_id else "en-US-Standard-A"
            )

            # Select the type of audio file you want returned
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000
            )

            # Perform the text-to-speech request
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )

            # Return the binary audio content
            return response.audio_content
        except Exception as e:
            print(f"Error synthesizing speech: {e}")
            return b""
