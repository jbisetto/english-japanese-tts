import nltk

def download_nltk_data():
    """Download required NLTK data packages."""
    print("Downloading NLTK data packages...")
    
    # The punkt tokenizer is used for sentence segmentation
    nltk.download('punkt')
    
    print("NLTK data packages downloaded successfully!")

if __name__ == "__main__":
    download_nltk_data() 