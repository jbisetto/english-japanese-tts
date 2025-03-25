import os
from typing import Tuple, Optional, List
from src.agent import TTSAgent
from src.config import Config

class GradioAdapter:
    def __init__(self, temp_dir: str):
        self.temp_dir = temp_dir
        os.makedirs(temp_dir, exist_ok=True)

    def create_config(self, tts_service: str, english_voice_id: str, 
                     japanese_voice_id: str, audio_format: str) -> Config:
        """Create a Config object based on user selections."""
        config = Config()
        config.tts_service = tts_service
        config.english_voice_id = english_voice_id
        config.japanese_voice_id = japanese_voice_id
        config.audio_format = audio_format
        return config

    def synthesize(self, text: str, tts_service: str, english_voice_id: str,
                  japanese_voice_id: str, audio_format: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Synthesize text to speech and return Gradio-compatible output.
        
        Returns:
            Tuple containing:
            - audio_path: Path to the generated audio file
            - segments_text: Formatted text showing language segments
            - error_message: Error message if any, None otherwise
        """
        try:
            # Create config and initialize agent
            config = self.create_config(tts_service, english_voice_id, japanese_voice_id, audio_format)
            agent = TTSAgent(config)

            # Generate output path
            output_path = os.path.join(self.temp_dir, f"output.{audio_format}")
            
            # Synthesize audio
            audio_path, segments = agent.synthesize(text, output_path)
            
            # Format segments for display
            segments_text = "\n".join(segments) if segments else text
            
            return audio_path, segments_text, None
            
        except Exception as e:
            print(f"Error in synthesis: {str(e)}")  # Debug print
            return None, None, str(e)

    def cleanup(self):
        """Clean up temporary audio files."""
        for filename in os.listdir(self.temp_dir):
            file_path = os.path.join(self.temp_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}") 