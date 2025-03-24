from setuptools import setup, find_packages

setup(
    name='english-japanese-tts',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'boto3',
        'pydub',
    ],
)
