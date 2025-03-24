class TextParser:
    def load_text(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        return text

    def preprocess_text(self, text: str) -> str:
        # Remove extra whitespace and newlines
        text = " ".join(text.split())
        return text
