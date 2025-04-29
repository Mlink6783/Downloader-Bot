import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import yt_dlp
import asyncio

# Your Telegram Bot Token
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# Health Check Function
async def health_check(context: ContextTypes.DEFAULT_TYPE):
    # Replace with your Telegram user ID (or a private chat ID)
    your_chat_id = 857216172  # <-- Change this to YOUR ID
    await context.bot.send_message(chat_id=your_chat_id, text="✅ Bot is alive and running!")

# Download function using yt-dlp
def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': '/tmp/%(title)s.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            return filename
    except Exception as e:
        print(f"Error downloading video: {str(e)}")
        return None

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a video link from YouTube, TikTok, or Facebook, and I'll download it for you!")

# /download command (for video download)
async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video_url = ' '.join(context.args)
    if not video_url:
        await update.message.reply_text("Please provide a video URL.")
        return

    try:
        video_file = download_video(video_url)
        if video_file:
            with open(video_file, 'rb') as video:
                await update.message.reply_video(video)
        else:
            await update.message.reply_text("Failed to download video.")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

# Main bot setup
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Adding Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("download", download))

    # Health check every 5 seconds
    app.job_queue.run_once(health_check, when=5)

    # Start polling
    await app.run_polling()

# Entry point
if __name__ == "__main__":
    # Get the current running event loop and run the bot
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
