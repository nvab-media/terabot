from pyrogram import Client, filters
import requests
import os
import logging
import threading
import time
from flask import Flask
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# Bot Configuration
API_ID = os.getenv("API_ID")  
API_HASH = os.getenv("API_HASH")  
BOT_TOKEN = os.getenv("BOT_TOKEN") 
PORT = int(os.getenv("PORT", 5000))
DL_IMAGE_LINK = "https://files.catbox.moe/4g27mb.jpg"
IMAGE_LINK = os.getenv("IMG_LINK", DL_IMAGE_LINK)
bot = Client("TerraboxBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

TERABOX_API_URL = "https://api-aswin-sparky.koyeb.app/api/downloader/terrabox?url="
# Flask app to keep the bot alive
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=PORT)

threading.Thread(target=run_flask, daemon=True).start()

@bot.on_message(filters.command("start"))
async def start(client, message):
    logging.info(f"User {message.from_user.id} started the bot.")
    await message.reply_photo(IMAGE_LINK, caption="Welcome to the Terabox Downloader Bot! \n\nSend me a Terabox link, and I'll download it for you!.\n\n---\nThis bot is provided by DOT-007❤️. Enjoy!")

@bot.on_message(filters.text & filters.private)
async def download_terrabox(client, message):
    url = message.text
    logging.info(f"Received URL from user {message.from_user.id}: {url}")
    
    if "http" not in url:
        logging.warning(f"Invalid URL received from user {message.from_user.id}")
        await message.reply_text("Please send a valid Terabox link.")
        return
    
    await message.reply_text("Downloading, please wait...")
    
    response = requests.get(TERABOX_API_URL + url)
    if response.status_code == 200:
        data = response.json()
        if data.get("status"):
            file_info = data.get("data", [])[0]
            file_url = file_info.get("downloadUrl")
            file_name = file_info.get("filename", "downloaded_file")
            
            if file_url:
                logging.info(f"Downloading file: {file_name} from {file_url}")
                file_response = requests.get(file_url, stream=True)
                file_path = f"downloads/{file_name}"
                os.makedirs("downloads", exist_ok=True)
                
                with open(file_path, "wb") as file:
                    for chunk in file_response.iter_content(1024):
                        file.write(chunk)
                
                await message.reply_document(file_path)
                logging.info(f"File {file_name} sent to user {message.from_user.id}")
                os.remove(file_path)
            else:
                logging.error("Failed to retrieve the download link.")
                await message.reply_text("Failed to retrieve the download link.")
        else:
            logging.error("Error in response data.")
            await message.reply_text("Error in response data.")
    else:
        logging.error("Error downloading from Terabox.")
        await message.reply_text("Error downloading from Terabox.")

bot.run()
