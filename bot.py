import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

BOT_TOKEN = "8536372437:AAEpxFAGpVpSgHrWiGhLLfQDyArEIqPrnSQ"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("မင်္ဂလာပါဆရာ။ ဒေါင်းလုဒ်ဆွဲချင်တဲ့ TikTok Video Link ကို ပို့ပေးပါ။")

async def download_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    
    if "tiktok.com" not in url:
        await update.message.reply_text("ကျေးဇူးပြု၍ မှန်ကန်သော TikTok Video Link ကို ပို့ပေးပါ။")
        return

    msg = await update.message.reply_text("ဗီဒီယိုကို စေခိုင်းထားသည့်အတိုင်း ဒေါင်းလုဒ်ဆွဲနေပါသည်။ ခဏစောင့်ပေးပါ။...")

    try:
        api_url = f"https://www.tikwm.com/api/?url={url}"
        response = requests.get(api_url).json()

        if response.get("code") == 0:
            video_url = response["data"]["play"]
            title = response["data"].get("title", "TikTok Video")

            await update.message.reply_video(video=video_url, caption=title)
            await msg.delete()
        else:
            await msg.edit_text("ဗီဒီယို ဒေါင်းလုဒ်ဆွဲ၍ မရပါ။ လင့်ခ်ကို ပြန်စစ်ပေးပါ။")
            
    except Exception as e:
        await msg.edit_text("အမှားတစ်ခု ဖြစ်ပေါ်ခဲ့ပါသည်။ နောက်မှ ပြန်လည်ကြိုးစားပါ။")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_tiktok))
    
    print("Bot စတင်အလုပ်လုပ်နေပါပြီ...")
    app.run_polling()
