import telebot
import yt_dlp
import os

TOKEN = "9060575501:AAHBFRqcuHJAB2VLs4eJusprhl5L_FYpXc8"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "اهلا بيك 🎬\nابعتلي لينك من تيك توك او انستا او فيس او يوتيوب وانا احملهولك")

@bot.message_handler(func=lambda m: True)
def download(message):
    url = message.text.strip()

    if "http" not in url:
        bot.reply_to(message, "ابعت لينك صحيح ❌")
        return

    bot.reply_to(message, "بحمل الفيديو... استنى شوية ⏳")

    try:
        # امسح اي فيديو قديم
        for f in os.listdir('.'):
            if f.startswith('video.'):
                os.remove(f)

        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': 'video.%(ext)s',
            'quiet': True,
            'noplaylist': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'الفيديو')

        for file in os.listdir('.'):
            if file.startswith('video.'):
                with open(file, 'rb') as f:
                    bot.send_video(message.chat.id, f, caption=title)
                os.remove(file)
                break
    except Exception as e:
        bot.reply_to(message, f"مقدرتش احمل اللينك ده 😢\nحاول لينك تاني")

print("Bot is running...")
bot.polling()
