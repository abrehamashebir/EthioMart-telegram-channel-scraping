import re

def _normalize_text(text):
        """Normalize text by removing special characters, extra spaces, etc."""
        text = text.strip()  # Remove leading/trailing spaces
        text = re.sub(r"[^\w\s፡።፣፤፥፦፧፨᎐᎑᎒]", "", text)  # Remove non-Amharic special characters
        text = re.sub(r"\s+", " ", text)  # Replace multiple spaces with a single space
        return text