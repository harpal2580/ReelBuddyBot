from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import instaloader
import os

# Initialize Instaloader
loader = instaloader.Instaloader()

# Start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "👋 Hi! Send me an Instagram link to download reels, posts, or stories!"
    )

# Help command
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "ℹ️ To use this bot:\n1️⃣ Send an Instagram link (reel, post, or story).\n2️⃣ I'll fetch and send the content back to you!"
    )

# Instagram download handler
def download_instagram(update: Update, context: CallbackContext) -> None:
    url = update.message.text.strip()
    chat_id = update.effective_chat.id

    # Validate URL
    if "instagram.com" not in url:
        update.message.reply_text("🚫 Please send a valid Instagram link.")
        return

    try:
        # Extract shortcode from URL
        shortcode = url.split("/")[-2]

        # Check if it's a video (reel or post) or story
        if 'reel' in url:
            # This handles Instagram Reels.
            post = instaloader.Post.from_shortcode(loader.context, shortcode)
            filename = f"{shortcode}.mp4" if post.is_video else f"{shortcode}.jpg"
            loader.download_post(post, target=f"{chat_id}")
        else:
            # Handling regular posts
            post = instaloader.Post.from_shortcode(loader.context, shortcode)
            filename = f"{shortcode}.mp4" if post.is_video else f"{shortcode}.jpg"
            loader.download_post(post, target=f"{chat_id}")

        # Check if it's a story
        if 'stories' in url:
            update.message.reply_text("Story download is not yet supported.")

        # Send downloaded file
        for file in os.listdir(f"{chat_id}"):
            with open(f"{chat_id}/{file}", 'rb') as content_file:
                update.message.reply_document(document=content_file)

        # Clean up
        for file in os.listdir(f"{chat_id}"):
            os.remove(f"{chat_id}/{file}")
        os.rmdir(f"{chat_id}")

    except Exception as e:
        update.message.reply_text(f"❌ Error: {e}")

# Main function
def main():
    TOKEN = "7709734303:AAEos3TsYspK-TLuzksM5O9EOelJEQ54M_A"  # Replace with your bot token
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, download_instagram))

    print("✅ Bot is running. Send /start to interact with it.")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
