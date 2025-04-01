import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

from src.agent import TTSAgent
from src.config import Config
from src.speech.exceptions import TTSError, TTSConnectionError

def main():
    # Load environment variables from .env file
    load_dotenv()

    try:
        # Initialize configuration and TTS agent
        config = Config()
        agent = TTSAgent(config)

        # Example text (mixed English and Japanese)
        text = "Hello, world. こんにちは、世界。"

        # Generate output path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(script_dir, "output.wav")

        # Synthesize speech
        print("Synthesizing speech...")
        audio_path, segments = agent.synthesize(text, output_path)
        
        # Print results
        print("\nText segments:")
        for segment in segments:
            print(f"- {segment}")
        
        print(f"\nAudio saved to: {audio_path}")

    except TTSConnectionError as e:
        print(f"Error connecting to TTS service: {e}")
        print("Please check your credentials and internet connection.")
    except TTSError as e:
        print(f"TTS error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
