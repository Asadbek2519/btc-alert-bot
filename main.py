import requests
import time
from telegram import Bot

# Telegram bot token va chat ID
TOKEN = '7651009437:AAGAgjLcBnkUGYhHpKYPfGLmKf8dyzA17Fo'
CHAT_ID = '437911645'

# Qidirilayotgan narx va juftlik
PAIR = 'BTCUSDT'
TARGET_PRICE = 95000

bot = Bot(token=TOKEN)

def get_price():
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={PAIR}'
    response = requests.get(url)
    data = response.json()
    return float(data['price'])

def main():
    alerted = False
    while not alerted:
        try:
            price = get_price()
            print(f"Current price: {price}")
            if price >= TARGET_PRICE:
                bot.send_message(chat_id=CHAT_ID, text=f"{PAIR} narxi {TARGET_PRICE}$ ga yetdi!")
                alerted = True
        except Exception as e:
            print(f"Xatolik: {e}")
        time.sleep(30)  # har 30 sekundda tekshirib turadi

if __name__ == '__main__':
    main()
