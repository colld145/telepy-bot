import os
import telebot
from telebot import types
import yt_dlp
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot("")


# @bot.message_handler(commands=['start'])
# def send_welcome(message):
# 	key = types.ReplyKeyboardMarkup(resize_keyboard=True)
# 	button1 = types.KeyboardButton("Download Movie")
# 	key.add(button1)
# 	bot.send_message(message.chat.id, "Hello, {0.first_name}. I'm {1.first_name}.".format(message.from_user, bot.get_me()), parse_mode="html", reply_markup=key)


@bot.message_handler(commands=["start"])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    download_video_button = telebot.types.KeyboardButton("🎥 Download Video")
    download_audio_button = telebot.types.KeyboardButton("🎵 Download Audio")
    download_video_playlist_button = telebot.types.KeyboardButton(
        "📄 Download Video Playlist"
    )
    download_audio_playlist_button = telebot.types.KeyboardButton(
        "📄 Download Audio Playlist"
    )
    keyboard.row(download_video_button, download_audio_button)
    keyboard.row(download_video_playlist_button, download_audio_playlist_button)

    bot.send_message(
        message.chat.id,
        """👋 Hello, {0.first_name}.\nEnter a button to work with functions of this bot 👇""".format(
            message.from_user, bot.get_my_description
        ),
        reply_markup=keyboard,
    )


@bot.message_handler(func=lambda message: message.text == "🎥 Download Video")
def handle_download_button(message):
    bot.send_message(message.chat.id, "🔗 Input an URL to download video:")

    bot.register_next_step_handler(message, handle_video_link)


def handle_video_link(message):
    url = message.text
    try:
        downloader_options = {
            "format": "best",
            "outtmpl": os.path.join("Downloads", "%(title)s.%(ext)s"),
        }
        downloader = yt_dlp.YoutubeDL(downloader_options)
        info = downloader.extract_info(url, download=False)
        downloader.download([url])

        video_file_path = os.path.join("Downloads", info["title"] + ".mp4")
        video_file = open(video_file_path, "rb")
        bot.send_video(message.chat.id, video_file)
    except Exception as error:
        bot.send_message(message.chat.id, f"❗ Error downloading video: {error}")


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.polling()
