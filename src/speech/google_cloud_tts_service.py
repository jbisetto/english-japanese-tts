import os
from google.cloud import texttospeech

class GoogleCloudTTSService:
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()

    def synthesize(self, language: str, text: str) -> bytes:
        """Synthesizes speech from the given text and language using Google Cloud TTS.

        Args:
            language: The language of the text.
            text: The text to synthesize.

        Returns:
            The synthesized audio data as bytes.
        """
        try:
            # Set the text input to be synthesized
            synthesis_input = texttospeech.SynthesisInput(text=text)

            # Build the voice request, select the language code ("en-US") and the ssml
            # voice gender ("neutral")
            voice = texttospeech.VoiceSelectionParams(
                language_code=language, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
            )

            # Select the type of audio file you want returned
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.LINEAR16
            )

            # Perform the text-to-speech request on the text input with the selected
            # voice parameters and audio file type
            response = self.client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )

            # The response's audio_content is binary.
            return response.audio_content
        except Exception as e:
            print(f"Error synthesizing speech: {e}")
            return b""
