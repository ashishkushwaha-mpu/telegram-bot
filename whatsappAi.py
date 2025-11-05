from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Import os for environment variables
import os

# Get token from environment variable
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("No TOKEN found in environment variables. Please set the TOKEN environment variable.")

# temporary user data store
user_data = {}

# Step 1 — Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 नमस्ते! मैं WhatsApp Link Generator Bot हूँ।\n\nकृपया Country Code भेजिए (उदा: 91 🇮🇳):")
    user_data[update.effective_user.id] = {"step": "cc"}

# Step 2 — Handle Messages Stepwise
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    data = user_data.get(user_id, {})

    if not data:
        await update.message.reply_text("कृपया /start से शुरू करें 🙂")
        return

    step = data.get("step")

    # Country Code Step
    if step == "cc":
        user_data[user_id]["cc"] = text
        user_data[user_id]["step"] = "phone"
        await update.message.reply_text("📞 अब कृपया Phone Number भेजिए (बिना + के):")
        return

    # Phone Step
    if step == "phone":
        user_data[user_id]["phone"] = text
        user_data[user_id]["step"] = "msg"
        await update.message.reply_text("💬 अब Message लिखिए (optional, कुछ नहीं भी लिख सकते हैं):")
        return

    # Message Step
    if step == "msg":
        cc = user_data[user_id]["cc"]
        phone = user_data[user_id]["phone"]
        msg = text

        # WhatsApp link generate
        from urllib.parse import quote
        link = f"https://api.whatsapp.com/send?phone={cc}{phone}&text={quote(msg)}"

        await update.message.reply_text(
            f"✅ आपका WhatsApp Link तैयार है:\n\n{link}\n\n📋 इसे कॉपी करें या क्लिक करें!"
        )

        user_data.pop(user_id, None)
        return

# Create Application
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("✅ WhatsApp Link Generator Telegram Bot चालू है...")
app.run_polling()
