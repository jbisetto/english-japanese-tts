## Architecture

The system is designed with a modular architecture, following a domain-driven design approach. The main components are:

### Text Processing Domain
- Handles text parsing and preprocessing
- Uses NLTK's PunktSentenceTokenizer for intelligent sentence segmentation
- Handles common abbreviations (Mr., Dr., Mrs., P.M., A.M., etc.)
- Provides clean text segments for language detection

### Language Detection Domain
- Detects the language of text segments using langdetect
- Supports English and Japanese language identification
- Handles mixed-language text by identifying language boundaries
- Returns language-tagged segments for appropriate voice selection

### Speech Synthesis Domain
- Converts text to speech using appropriate models/voices
- Supports multiple TTS services:
  - AWS Polly: Primary service for both English and Japanese
  - Google Cloud TTS: Alternative service with neural voices
- Implements robust error handling:
  - TTSConnectionError: For service connection issues
  - TTSInvalidInputError: For invalid text or parameters
  - TTSSynthesisError: For synthesis failures
  - TTSError: For general TTS-related issues

### Output Domain
- Manages audio processing and format conversion
- Supports multiple output formats (WAV, MP3, OGG)
- Handles segment merging with natural transitions
- Ensures consistent audio quality across segments

### Service Integration Layer
- AWS Polly Integration:
  - Provides text-to-speech synthesis for both English and Japanese
  - Supports multiple voices per language
  - Handles API authentication and rate limiting
- Google Cloud TTS Integration:
  - Offers neural voice alternatives
  - Supports advanced speech synthesis features
  - Manages service account authentication

### System Orchestration
The `TTSAgent` orchestrates the entire process:
1. Text preprocessing and segmentation
2. Language detection for each segment
3. TTS service selection and synthesis
4. Audio merging and format conversion
5. Error handling and recovery

### Error Handling
The system implements a comprehensive error handling strategy:
- Input validation at each processing stage
- Service-specific error handling
- Graceful degradation when services are unavailable
- Detailed error reporting for debugging

### Data Flow
```
[Input Text] → [Text Processing] → [Language Detection] → [TTS Service Selection]
     ↓
[Speech Synthesis] → [Audio Processing] → [Format Conversion] → [Final Output]
```
