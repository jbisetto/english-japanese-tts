import os

class Config:
    def __init__(self):
        self.english_voice_id = os.environ.get("ENGLISH_VOICE_ID", "Emma")
        self.japanese_voice_id = os.environ.get("JAPANESE_VOICE_ID", "Takumi")
        self.tts_service = os.environ.get("TTS_SERVICE", "aws_polly") # Options: aws_polly, google_cloud
        
        # AWS credentials
        self.aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
        self.aws_region_name = os.environ.get("AWS_REGION_NAME", "us-east-1")
