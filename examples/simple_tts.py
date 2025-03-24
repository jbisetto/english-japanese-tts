from src.agent import TTSAgent
from src.config import Config

def main():
    config = Config()
    agent = TTSAgent(config)
    text = "Hello, world. こんにちは、世界。"
    output_path = "output.mp3"
    agent.synthesize(text, output_path)
    print(f"Audio saved to {output_path}")

if __name__ == "__main__":
    main()
