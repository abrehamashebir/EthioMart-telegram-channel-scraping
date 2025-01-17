import json
import os
from scripts.data_preprocessor import DataPreprocessor
from scripts.scraping_telegram import TelegramScraper

def load_metadata(file_path):
    """Load metadata from a JSON file."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_metadata(file_path, data):
    """Save metadata to a JSON file."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def fetch_data(scraper, channels, metadata_file, raw_data_folder):
    """Fetch data and update metadata."""
    metadata = load_metadata(metadata_file)
    os.makedirs(raw_data_folder, exist_ok=True)

    for channel in channels:
        print(f"Fetching messages from {channel}...")
        last_fetched_id = metadata.get(channel, {}).get("last_fetched_id")
        messages = scraper.fetch_messages(channel, limit=200, min_id=last_fetched_id)

        if messages:
            # Save fetched messages
            file_name = os.path.join(raw_data_folder, f"{channel[1:]}.json")
            with open(file_name, "w", encoding="utf-8") as f:
                json.dump(messages, f, ensure_ascii=False, indent=4)
                print(f"Messages from {channel} saved to '{file_name}'.")

            # Update metadata with the latest fetched message ID
            metadata[channel] = {
                "last_fetched_id": messages[0]["id"],  # Assume messages are sorted by ID
                "last_fetched_time": messages[0]["timestamp"]
            }
        else:
            print(f"No new messages found for {channel}.")

    save_metadata(metadata_file, metadata)

def preprocess_data(preprocessor, raw_data_folder, preprocessed_data_folder, metadata_file):
    """Preprocess data and update metadata."""
    metadata = load_metadata(metadata_file)
    os.makedirs(preprocessed_data_folder, exist_ok=True)

    for file_name in os.listdir(raw_data_folder):
        if file_name.endswith(".json"):
            channel = f"@{os.path.splitext(file_name)[0]}"
            input_file = os.path.join(raw_data_folder, file_name)
            output_file = os.path.join(preprocessed_data_folder, file_name)

            last_preprocessed_id = metadata.get(channel, {}).get("last_preprocessed_id")

            with open(input_file, "r", encoding="utf-8") as f:
                messages = json.load(f)

            # Filter messages for preprocessing
            new_messages = [
                msg for msg in messages
                if last_preprocessed_id is None or msg["id"] > last_preprocessed_id
            ]

            if new_messages:
                print(f"Preprocessing new messages for {channel}...")
                processed_messages = [preprocessor.preprocess_message(msg) for msg in new_messages]


                # Save preprocessed data
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(processed_messages, f, ensure_ascii=False, indent=4)
                    print(f"Preprocessed data for {channel} saved to '{output_file}'.")

                # Update metadata with the latest preprocessed message ID
                metadata[channel] = {
                    "last_preprocessed_id": new_messages[-1]["id"]
                }
            else:
                print(f"No new messages to preprocess for {channel}.")

    save_metadata(metadata_file, metadata)

def main():
    # Directory setup
    raw_data_folder = "data/raw"
    preprocessed_data_folder = "data/preprocessed"
    metadata_fetch_file = "metadata/last_fetched.json"
    metadata_preprocess_file = "metadata/last_preprocessed.json"

    os.makedirs("metadata", exist_ok=True)

    # Telegram scraping
    channels = [ 
        "@nevacomputer"
    ]
    scraper = TelegramScraper()


    try:
        fetch_data(scraper, channels, metadata_fetch_file, raw_data_folder)
    except Exception as e:
        print(f"An error occurred during data fetching: {e}")
    finally:
        scraper.close()

    # Preprocessing
    try:
        preprocessor = DataPreprocessor(raw_data_folder, preprocessed_data_folder)
        preprocess_data(preprocessor, raw_data_folder, preprocessed_data_folder, metadata_preprocess_file)
    except Exception as e:
        print(f"An error occurred during data preprocessing: {e}")

if __name__ == "__main__":
    main()
