import os

class Config:
    def __init__(self):
        self.bedrock_region = os.environ.get("BEDROCK_REGION", "us-east-1")
        self.english_voice_id = os.environ.get("ENGLISH_VOICE_ID", "Emma")
        self.japanese_voice_id = os.environ.get("JAPANESE_VOICE_ID", "Takumi")
        self.language_detection_model_id = os.environ.get("LANGUAGE_DETECTION_MODEL_ID", "amazon.titan-text-large")
        self.tts_service = os.environ.get("TTS_SERVICE", "aws_polly") # Options: aws_polly, google_cloud
