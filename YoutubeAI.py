import os
import asyncio
import tempfile
from pathlib import Path
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler

# ========== CONFIG ==========
# 🔹 Replace with your actual BotFather token
TELEGRAM_TOKEN = "8354491526:AAEcuhonmYg7MAShGDOVMZ2g5tr3UGRprmU"

# 🔹 Full path to yt-dlp.exe (change this path according to your system)
YTDLP_PATH = r"C:\Users\ASHISH KUSHWAHA\AppData\Local\Programs\Python\Python311\Scripts\yt-dlp.exe"

# 🔹 File size limit (Telegram bot limit = ~50 MB for normal bots)
MAX_SEND_SIZE = 50 * 1024 * 1024  # 50 MB
# =============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! Send me a video link (YouTube, Instagram, etc.) and I'll download it for you."
    )

def is_probable_url(text: str) -> bool:
    return text.startswith("http://") or text.startswith("https://")

async def download_with_ytdlp(url: str, outdir: Path) -> Path:
    """Download video using yt-dlp with full path to exe."""
    out_template = str(outdir / "%(title).200s.%(ext)s")

    cmd = [
        YTDLP_PATH,  # direct path to yt-dlp.exe
        "-f", "bestvideo+bestaudio/best",
        "--merge-output-format", "mp4",
        "-o", out_template,
        url,
    ]

    proc = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()

    # check if something downloaded
    files = sorted(outdir.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True)
    for f in files:
        if f.is_file():
            return f

    raise FileNotFoundError(f"yt-dlp failed:\n{stderr.decode() or stdout.decode()}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()
    if not text:
        await update.message.reply_text("⚠️ Please send a video link.")
        return

    if not is_probable_url(text):
        await update.message.reply_text("⚠️ Please send a valid URL (starting with http:// or https://).")
        return

    msg = await update.message.reply_text("⏳ Downloading... Please wait a few moments.")

    try:
        with tempfile.TemporaryDirectory() as tmpdirname:
            outdir = Path(tmpdirname)
            downloaded_file = await download_with_ytdlp(text, outdir)
            size = downloaded_file.stat().st_size

            if size > MAX_SEND_SIZE:
                await update.message.reply_text(
                    f"❗ File is too large ({size/1024/1024:.1f} MB). Telegram allows only up to 50 MB.\n"
                    "Try sending a shorter video link or use a clip-downloader website."
                )
                await update.message.reply_text(f"Filename: {downloaded_file.name}")
            else:
                await update.message.reply_video(video=open(downloaded_file, "rb"), filename=downloaded_file.name)
    except Exception as e:
        await update.message.reply_text(f"❌ Error while downloading: {e}")
    finally:
        try:
            await msg.delete()
        except Exception:
            pass

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("✅ Bot running... Send /start in Telegram to test.")
    app.run_polling()

if __name__ == "__main__":
    main()
