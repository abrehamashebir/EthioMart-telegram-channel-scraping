from telethon import TelegramClient
import csv
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')
phone = os.getenv('phone')

async def scrape_channel(client, channel_username, writer, media_dir):
    try:
        entity = await client.get_entity(channel_username)
        channel_title = entity.title
        async for message in client.iter_messages(entity, limit=200):  # Adjust limit as needed
            media_path = None
            try:
                if message.media:
                    if hasattr(message.media, 'photo'):
                        filename = f"{channel_username}_{message.id}.jpg"
                    elif hasattr(message.media, 'video'):
                        filename = f"{channel_username}_{message.id}.mp4"
                    else:
                        filename = None

                    if filename:
                        media_path = os.path.join(media_dir, filename)
                        await client.download_media(message.media, media_path)
            except Exception as e:
                print(f"Error downloading media: {e}")
            message_text = message.message if message.message else "[No Text]"
            writer.writerow([channel_title, channel_username, message.id, message_text, message.date, media_path])
    except Exception as e:
        print(f"Failed to scrape {channel_username}: {e}")

client = TelegramClient('scraping_session', api_id, api_hash)

async def main():
    await client.start()
    media_dir = 'photos'
    os.makedirs(media_dir, exist_ok=True)
    
    with open('./datasets/telegram_data.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if os.stat('./datasets/telegram_data.csv').st_size == 0:
            writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path'])
        
        channels = ['@nevacomputer']  # Add your channels
        for channel in channels:
            await scrape_channel(client, channel, writer, media_dir)
            print(f"Scraped data from {channel}")

with client:
    client.loop.run_until_complete(main())
