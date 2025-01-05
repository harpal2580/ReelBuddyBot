from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
import instaloader
import os

# Initialize Instaloader
loader = instaloader.Instaloader()

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hi! Send me an Instagram link to download reels, posts, or stories!")

# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ℹ️ To use this bot:\n1️⃣ Send an Instagram link (reel, post, or story).\n2️⃣ I'll fetch and send the content back to you!")

# Instagram download handler
async def download_instagram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    chat_id = update.effective_chat.id

    # Validate URL
    if "instagram.com" not in url:
        await update.message.reply_text("🚫 Please send a valid Instagram link.")
        return

    try:
        # Extract shortcode from URL
        shortcode = url.split("/")[-2]

        # Fetch and download post
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        filename = f"{shortcode}.mp4" if post.is_video else f"{shortcode}.jpg"

        loader.download_post(post, target=f"{chat_id}")

        # Send downloaded file
        for file in os.listdir(f"{chat_id}"):
            with open(f"{chat_id}/{file}", 'rb') as content_file:
                await update.message.reply_document(document=content_file)

        # Clean up
        for file in os.listdir(f"{chat_id}"):
            os.remove(f"{chat_id}/{file}")
        os.rmdir(f"{chat_id}")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# Main function
def main():
    TOKEN = "7709734303:AAEos3TsYspK-TLuzksM5O9EOelJEQ54M_A"
    app = ApplicationBuilder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_instagram))

    print("✅ Bot is running. Send /start to interact with it.")
    app.run_polling()

if __name__ == "__main__":
    main()
