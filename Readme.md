# Terabox Downloader Bot

A simple **Telegram bot** for downloading files from **Terabox** using **Pyrogram**.

## Features

✅ Download files from Terabox
✅ Send files directly to Telegram
✅ Easy-to-use bot commands
✅ Supports multiple file formats
✅ Deployable on **Heroku, VPS, or locally**

## Requirements

- Python 3.8+
- `pip install -r requirements.txt`
- Telegram Bot API key from [@BotFather](https://t.me/BotFather)
- `API_ID` and `API_HASH` from [my.telegram.org](https://my.telegram.org/apps)

## Installation

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/nvab-media/terabot.git
cd terabot
```

### 2️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 3️⃣ Configure Environment Variables
Create a `.env` file and add the following:
## env
> | Variable   | Description |
> |------------|-------------|
> | `API_ID`   | Your Telegram API ID |
> | `API_HASH` | Your Telegram API Hash |
> | `BOT_TOKEN` | The bot token from @BotFather |
> | `IMG_LINK` |  your IMG URL |
> | `PORT` | (5000) |


### 4️⃣ Run the Bot
```sh
python tera.py
```


# Depoly to koyeb
[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?type=git&builder=dockerfile&repository=https://github.com/nvab-media/terabot&branch=main&name=DotserModz&env[API_ID]=your_api_id&env[API_HASH]=your_api_hash&env[BOT_TOKEN]=your_bot_token&env[PORT]=8000)


# Depoly to Render
[![Deploy](https://img.shields.io/badge/-Deploy-black?style=for-the-badge&logo=Render&logoColor=white)](https://render.com/deploy?repo=https://github.com/nvab-media/terabot)

Deployment Instructions
1. Fork this repo Click Here
2. On Render dashboard, click New and choose Web Service.
3. Choose Public Repository, then paste this url: https://github.com/nvab-media/terabot
4. Add required environment variables.

> ## Add .env ⬇️
> | Variable   | Description |
> |------------|-------------|
> | `API_ID`   | Your Telegram API ID |
> | `API_HASH` | Your Telegram API Hash |
> | `BOT_TOKEN` | The bot token from @BotFather |
> | `IMG_LINK` |  your IMG URL |
> | `PORT` | (5000) |

## Contributing

Feel free to fork this repository and submit pull requests. Contributions are welcome!

## License

This project is licensed under the **MIT License**.

---

### 🌟 Star this repo if you found it useful!
