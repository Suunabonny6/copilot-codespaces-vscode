import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from moviepy.video.io.VideoFileClip import VideoFileClip
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("7378342501:AAF0n0y8uz9n4GfBxf5fjxMro5LtivNCrG8")

# Start command handler
async def start(update: Update, context):
    await update.message.reply_text("Welcome! Send me a video, and I'll compress it for you.")

# Video message handler
async def handle_video(update: Update, context):
    video_file = await update.message.video.get_file()
    input_path = "input_video.mp4"
    output_path = "compressed_video.mp4"

    # Download the video
    await video_file.download_to_drive(input_path)

    # Compress the video
    video = VideoFileClip(input_path)
    video_resized = video.resize(height=480)  # Resize to 480p
    video_resized.write_videofile(output_path, bitrate="500k")  # Compress with 500k bitrate
    video.close()

    # Send the compressed video back
    await update.message.reply_video(video=open(output_path, "rb"))

    # Clean up temporary files
    os.remove(input_path)
    os.remove(output_path)

# Main function to run the bot
def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
