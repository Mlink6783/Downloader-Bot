import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import yt_dlp

# Your Telegram Bot Token
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# Download function using yt-dlp
def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': '/tmp/%(title)s.%(ext)s',  # Temporary file save location
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info_dict)
        return filename

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
        with open(video_file, 'rb') as video:
            await update.message.reply_video(video)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

# Main bot setup
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("download", download))

app.run_polling()

