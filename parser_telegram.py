import os
import requests
from bs4 import BeautifulSoup
from telegram import Bot
import time

TOKEN = os.getenv('TELEGRAM_TOKEN')  
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')  

KEYWORDS = ['автокресло', 'коляска']

def parse_website():
    url = "https://www.kufar.by/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Не удалось получить доступ к сайту")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    new_ads = []

    # check class
    ads = soup.find_all("a", class_="search-item__link")
    
    for ad in ads:
        ad_title = ad.get_text(strip=True)
        ad_url = ad['href']

        # check keyword
        if any(keyword.lower() in ad_title.lower() for keyword in KEYWORDS):
            new_ads.append((ad_title, ad_url))

    return new_ads

def send_telegram_message(bot, message):
    bot.send_message(chat_id=CHAT_ID, text=message)

def main():
    bot = Bot(token=TOKEN)

    last_seen_ads = set()  
    while True:
        new_ads = parse_website()

        # уведомления
        for ad in new_ads:
            if ad not in last_seen_ads:
                message = f"Новое объявление: {ad[0]}\n{ad[1]}"
                send_telegram_message(bot, message)
                last_seen_ads.add(ad)

        # Пауза 
        time.sleep(900)

if __name__ == "__main__":
    main()
