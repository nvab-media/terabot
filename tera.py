from pyrogram import Client, filters
import requests
import os
import logging
import threading
import asyncio
from flask import Flask
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables
load_dotenv()

# Bot Configuration
API_ID = os.getenv("API_ID")  
API_HASH = os.getenv("API_HASH")  
BOT_TOKEN = os.getenv("BOT_TOKEN") 
PORT = int(os.getenv("PORT", 5000))

DL_IMAGE_LINK = "https://files.catbox.moe/4g27mb.jpg"
IMAGE_LINK = os.getenv("IMG_LINK", DL_IMAGE_LINK)
TERABOX_API_URL = "https://ironman.koyeb.app/ironman/dl/terabox?link="

# Initialize bot
bot = Client("TerraboxBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Flask app to keep the bot running
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

# Run Flask in a separate thread
def run_flask():
    app.run(host="0.0.0.0", port=PORT, threaded=True)

threading.Thread(target=run_flask, daemon=True).start()

# Start command handler
@bot.on_message(filters.command("start"))
async def start(client, message):
    logging.info(f"User {message.from_user.id} started the bot.")
    await message.reply_photo(
        IMAGE_LINK, 
        caption="Welcome to the Terabox Downloader Bot! \n\nSend me a Terabox link, and I'll download it for you!\n\n---\nThis bot is provided by DOT-007❤️. Enjoy!"
    )

# Function to handle Terabox download requests
@bot.on_message(filters.text & filters.private)
async def download_terrabox(client, message):
    url = message.text.strip()
    logging.info(f"Received URL from user {message.from_user.id}: {url}")

    if not url.startswith("http"):
        await message.reply_text("🚨 Invalid link! Please send a valid Terabox link.")
        return

    await message.reply_text("⏳ Fetching the download link, please wait...")

    try:
        # Fetch API response
        response = requests.get(TERABOX_API_URL + url, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors

        data = response.json()

        # Check if API returns "not found"
        if data.get("message") == "not found":
            await message.reply_text("❌ The requested file was not found on Terabox.")
            return

        # Extract file details
        file_url = data.get("dlink")
        file_name = data.get("filename", "downloaded_file.mp4")  # Default name if missing
        file_size = data.get("size", "Unknown size")

        if not file_url:
            await message.reply_text("❌ Unable to retrieve a valid download link.")
            return

        logging.info(f"Downloading file: {file_name} (Size: {file_size}) from {file_url}")
        await message.reply_text(f"📥 Downloading `{file_name}`...")

        file_path = f"downloads/{file_name}"
        os.makedirs("downloads", exist_ok=True)

        # Asynchronous file download
        async def download_file():
            with requests.get(file_url, stream=True) as file_response:
                file_response.raise_for_status()
                with open(file_path, "wb") as file:
                    for chunk in file_response.iter_content(1024):
                        file.write(chunk)

        await asyncio.to_thread(download_file)

        # Send the file to the user
        await message.reply_document(file_path, caption=f"🎉 Here is your file: `{file_name}`")
        logging.info(f"File `{file_name}` sent to user {message.from_user.id}")

        # Clean up downloaded file
        os.remove(file_path)

    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {e}")
        await message.reply_text("🚨 Error fetching the download link. Please try again later.")
    
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        await message.reply_text("❌ An unexpected error occurred.")

# Run the bot
bot.run()
