import logging
import requests
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import threading
import time

# Telegram token va chat_id kerak bo'ladi
TOKEN = '7651009437:AAGAgjLcBnkUGYhHpKYPfGLmKf8dyzA17Fo'
bot = Bot(token=TOKEN)

# Har bir foydalanuvchining kuzatuv ro'yxati (juftlik, narx)
alerts = {}

logging.basicConfig(level=logging.INFO)

def get_price(pair):
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={pair.upper()}'
    response = requests.get(url)
    return float(response.json()['price'])

def price_checker():
    while True:
        for chat_id in list(alerts):
            to_remove = []
            for pair, target in alerts[chat_id]:
                try:
                    price = get_price(pair)
                    if price >= target:
                        bot.send_message(chat_id=chat_id, text=f"{pair} narxi {target}$ ga yetdi! (Hozirgi narx: {price})")
                        to_remove.append((pair, target))
                except Exception as e:
                    print(f"Xatolik: {e}")
            for item in to_remove:
                alerts[chat_id].remove(item)
        time.sleep(30)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Coin narx signal uchun bu formatda yozing:\n\nBTC.USDT.95000")

def handle_message(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text.replace(" ", "")
    try:
        symbol, currency, price = text.upper().split(".")
        pair = symbol + currency
        price = float(price)

        if chat_id not in alerts:
            alerts[chat_id] = []
        alerts[chat_id].append((pair, price))
        update.message.reply_text(f"{pair} narxi {price}$ ga yetganda sizga xabar beraman.")
    except:
        update.message.reply_text("Xato format! To'g'ri format: COIN.USDT.NARX\nMasalan: BTC.USDT.95000")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    threading.Thread(target=price_checker, daemon=True).start()

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
