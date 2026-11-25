import os
import telebot
import yt_dlp
import requests

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def start(m):
    bot.reply_to(m, "ابعت لينك TikTok او Facebook وانا احملهولك 🎥")

@bot.message_handler(func=lambda m: True)
def download(m):
    url = m.text.strip()
    if "tiktok.com" not in url and "facebook.com" not in url and "fb.watch" not in url:
        bot.reply_to(m, "ابعت لينك TikTok او Facebook صحيح")
        return
    bot.reply_to(m, "بحمل... استنى ثواني ⏳")
    # محاولة سريعة للتيك توك من tikwm
    if "tiktok.com" in url:
        try:
            r = requests.get(f"https://www.tikwm.com/api/?url={url}", timeout=20).json()
            video = r.get("data", {}).get("play")
            if video:
                bot.send_video(m.chat.id, video)
                return
        except:
            pass
    # تحميل بـ yt-dlp
    try:
        ydl_opts = {'format': 'mp4', 'outtmpl': 'video.mp4', 'quiet': True, 'noplaylist': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        with open('video.mp4','rb') as f:
            bot.send_video(m.chat.id, f)
        os.remove('video.mp4')
    except Exception as e:
        bot.reply_to(m, "مش عارف احمل الفيديو ده، جرب واحد تاني")

bot.polling()
