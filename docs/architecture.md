## Architecture

The system is designed with a modular architecture, following a domain-driven design approach. The main components are:

-   **Text Processing Domain**: Handles text parsing and preprocessing.
-   **Language Detection Domain**: Detects the language of text segments.
-   **Speech Synthesis Domain**: Converts text to speech using appropriate models/voices.
-   **Output Domain**: Manages audio merging and output formatting.
-   **AWS Integration**: Provides the Amazon Bedrock client for API communication.

The `TTSAgent` orchestrates the entire process, coordinating the workflow between components.
