import os
from src.agent import TTSAgent
from src.config import Config

def main():
    config = Config()
    agent = TTSAgent(config)
    text = "Hello, world. こんにちは、世界。"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "output.wav")
    agent.synthesize(text, output_path)
    if os.path.exists(output_path):
        print(f"Audio saved to {output_path}")
    else:
        print(f"Error: Audio file not saved to {output_path}")

if __name__ == "__main__":
    main()
