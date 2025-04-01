from setuptools import setup, find_packages

setup(
    name='english-japanese-tts',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'boto3',
        'pydub',
        'google-cloud-texttospeech',
        'numpy',
        'librosa',
        'soundfile',
        'langdetect',
        'ffmpeg-python',
        'nltk>=3.8.1',
    ],
)
