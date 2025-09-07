import os
import time
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# Список товаров для отслеживания
URLS = [
    {
        "url": "https://store.steampowered.com/app/1091500/Cyberpunk_2077/",
        "selector": ".discount_pct",   # селектор скидки
        "min_discount": 30
    },
    {
        "url": "https://www.aliexpress.com/item/1005005182236977.html",
        "selector": ".product-price-value",  # цена
        "min_discount": 20
    }
]

def send_message(text: str):
    """Отправка сообщения в Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def check_price(item):
    """Проверка скидки/цены на странице"""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(item["url"], headers=headers, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        elem = soup.select_one(item["selector"])
        if not elem:
            return f"❌ Не нашёл цену для {item['url']}"

        text = elem.get_text(strip=True)
        return f"✅ {item['url']} → {text}"

    except Exception as e:
        return f"⚠️ Ошибка при проверке {item['url']}: {e}"

def main():
    while True:
        for item in URLS:
            msg = check_price(item)
            send_message(msg)
        time.sleep(3600)  # проверка раз в час

if __name__ == "__main__":
    main()
