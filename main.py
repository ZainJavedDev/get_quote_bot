import os
import requests
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
DISCORD_WEBHOOK_ID = os.getenv("DISCORD_WEBHOOK_ID")
DISCORD_WEBHOOK_TOKEN = os.getenv("DISCORD_WEBHOOK_TOKEN")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")


def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    quote_text = response.json()[0]['q']
    credit = response.json()[0]['a']

    unsplash_response = requests.get(f'https://api.unsplash.com/search/photos/?query={credit}&client_id={UNSPLASH_ACCESS_KEY}')
    best_image = unsplash_response.json()['results'][0]['urls']['small']
    
    store(quote_text, credit, best_image)
    send_webhook_message(quote_text, credit, best_image)

def store(quote_text, credit, best_image):
    db = mysql.connector.connect(host="localhost", user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DATABASE)
    
    sql = "DELETE FROM quote"
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()

    cursor = db.cursor()
    sql = "INSERT INTO quote (`quote_text`, `credit`, `image`) VALUES (%s, %s, %s)"
    val = (quote_text, credit, best_image)
    cursor.execute(sql, val)
    db.commit()
    

def send_webhook_message(quote_text, credit, best_image):

    webhook_url= f'https://discord.com/api/webhooks/{DISCORD_WEBHOOK_ID}/{DISCORD_WEBHOOK_TOKEN}'

    data = {
        "embeds": [
            {
                "title":quote_text,
                "description": f"- {credit}",
                "image": {
                    "url": best_image
                }
            }
        ]
    }
    requests.post(webhook_url, json=data)


def main():
    get_quote()

if __name__ == "__main__":
    main()
