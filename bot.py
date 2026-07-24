
import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://www.men.gov.ma/"

LAST_FILE = "last_news.txt"


def get_latest_news():
    response = requests.get(URL, timeout=20)
    soup = BeautifulSoup(response.text, "html.parser")

    for link in soup.find_all("a", href=True):
        title = link.get_text(strip=True)
        href = link["href"]

        if len(title) > 20:
            if href.startswith("/"):
                href = "https://www.men.gov.ma" + href
            return title, href

    return None, None


def send_message(message):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message,
            "disable_web_page_preview": False
        }
    )


title, url = get_latest_news()

if title:
    old = ""

    if os.path.exists(LAST_FILE):
        with open(LAST_FILE, "r", encoding="utf-8") as f:
            old = f.read().strip()

    if old != url:
        send_message(f"📢 خبر جديد من وزارة التربية الوطنية\n\n{title}\n\n{url}")

        with open(LAST_FILE, "w", encoding="utf-8") as f:
            f.write(url)
