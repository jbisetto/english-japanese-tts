## Usage Guide

### Basic Usage

The system can be used either through the command-line interface or the demo web application.

#### Command Line Interface

```python
from src.speech.tts_agent import TTSAgent

# Initialize the TTS agent
agent = TTSAgent()

# Simple synthesis
text = "Hello! こんにちは！"
output_path = "output.mp3"
agent.synthesize(text, output_path)
```

### Mixed Language Examples

```python
# Multiple sentences with different languages
text = """
Hello! How are you today? 
こんにちは！お元気ですか？
I am learning Japanese. 日本語を勉強しています。
"""

# The system will automatically:
# 1. Detect language boundaries
# 2. Split into appropriate segments
# 3. Use the correct voice for each language
agent.synthesize(text, "mixed_language.mp3")

# Handling abbreviations
text = "Dr. Smith visited Mt. Fuji at 2 P.M. 富士山は美しいです。"
agent.synthesize(text, "abbreviations.mp3")
```

### Error Handling

```python
from src.speech.exceptions import TTSConnectionError, TTSInvalidInputError

try:
    agent.synthesize(text, output_path)
except TTSConnectionError as e:
    print(f"Connection error: {e}")
    # Handle connection issues
except TTSInvalidInputError as e:
    print(f"Invalid input: {e}")
    # Handle invalid input
except Exception as e:
    print(f"Unexpected error: {e}")
    # Handle other errors
```

### Development and Testing

Run the test suite:
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_language.py -v

# Run with coverage
python -m pytest tests/ --cov=src/
```

### Advanced Usage

#### Custom Voice Selection

```python
# Initialize with specific voices
agent = TTSAgent(
    english_voice_id="Matthew",
    japanese_voice_id="Mizuki"
)
```

#### Output Format Selection

```python
# Specify output format
agent.synthesize(text, "output.wav", format="wav")  # WAV format
agent.synthesize(text, "output.mp3", format="mp3")  # MP3 format
agent.synthesize(text, "output.ogg", format="ogg")  # OGG format
```

### Best Practices

1. **Text Preparation**
   - Use proper punctuation
   - Avoid mixing languages mid-sentence
   - Include appropriate spacing between languages

2. **Error Handling**
   - Always implement proper error handling
   - Check for service availability
   - Validate input text

3. **Resource Management**
   - Clean up temporary files
   - Monitor API usage
   - Handle rate limiting
