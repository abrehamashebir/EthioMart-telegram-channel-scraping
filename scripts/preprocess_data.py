import re
import pandas as pd

def clean_message_column(df, column_name='Message'):
    """
    Cleans the specified column in the DataFrame by removing unwanted characters.

    Args:
        df (pd.DataFrame): Input DataFrame with the column to clean.
        column_name (str): Name of the column to clean. Default is 'Message'.

    Returns:
        pd.DataFrame: DataFrame with the cleaned column.
    """
    def remove_unwanted_characters(text):
        # Define a regex pattern to remove unwanted characters (e.g., emojis, special symbols)
        pattern = r'[^\w\s]'  # Keeps only alphanumeric characters and spaces
        cleaned_text = re.sub(pattern, '', text) if isinstance(text, str) else text
        return cleaned_text

    # Apply the cleaning function to the specified column
    df[column_name] = df[column_name].apply(remove_unwanted_characters)
    return df

def clean_text(text):
        if isinstance(text, str):  # Ensure the value is a string
            # Remove special characters (except alphanumeric and spaces)
            text = re.sub(r'[^\w\s]', '', text)
            # Replace newlines with a space
            text = text.replace('\n', ' ')
            # Collapse multiple spaces into a single space
            text = re.sub(r'\s+', ' ', text)
            # Strip leading/trailing spaces
            return text.strip()
        return text
