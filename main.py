import os
import telebot
import yt_dlp
import tempfile
import shutil

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "ابعت لينك من TikTok / Facebook / YouTube / Instagram\nوهنزلهولك من غير علامة مائية 🎬")

@bot.message_handler(func=lambda m: True)
def download(message):
    url = message.text.strip()
    if "http" not in url:
        bot.reply_to(message, "ابعت لينك صحيح ❌")
        return

    msg = bot.reply_to(message, "جارٍ التحميل... ⏳")
    tmpdir = tempfile.mkdtemp()

    ydl_opts = {
        'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'extractor_args': {'tiktok': {'api_hostname': 'api16-normal-c-useast1a.tiktokv.com'}},
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # لو البوست فيه صور وفيديوهات كتير
            if 'entries' in info:
                files = []
                for entry in info['entries']:
                    if entry:
                        files.append(ydl.prepare_filename(entry))
            else:
                files = [ydl.prepare_filename(info)]

        for file_path in files:
            if not os.path.exists(file_path):
                # جرب نلاقي اي ملف اتحمل
                continue
            if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                with open(file_path, 'rb') as f:
                    bot.send_photo(message.chat.id, f)
            elif file_path.lower().endswith(('.mp4', '.mov', '.webm', '.mkv')):
                with open(file_path, 'rb') as f:
                    bot.send_video(message.chat.id, f)
            else:
                with open(file_path, 'rb') as f:
                    bot.send_document(message.chat.id, f)

        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"حصل خطأ ❌\n{e}\nجرب لينك تاني", message.chat.id, msg.message_id)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

print("Bot is running...")
bot.infinity_polling()
