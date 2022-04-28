class UnsupportedLanguageException(ValueError):
    """Exception raised when a user tries to configure a language that we don't support"""
    def __init__(self, language: str):
        super().__init__(f"Unsupported language: {language}")
