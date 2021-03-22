# http://quotes.toscrape.com

import requests
from bs4 import BeautifulSoup
from time import sleep
from csv import DictWriter

all_quotes = []

base_url = "http://quotes.toscrape.com"
url = "/page/1"

while url:

    res = requests.get(f"{base_url}{url}")
    res.encoding = "utf-8"
    print(f"Now Scraping {base_url}{url}")
    soup = BeautifulSoup(res.text, "html.parser")

    quotes = soup.find_all(class_="quote")

    for quote in quotes:
        all_quotes.append({"Text": quote.find(class_="text").get_text(),
                           "Author": quote.find(class_="author").get_text(),
                           "Bio-Link": quote.find("a")["href"]
                           })

    next_button = soup.find(class_="next")
    url = next_button.find("a")["href"] if next_button else None
    sleep(3)


# write to CSV file
with open("quotes.csv", "w", encoding="utf-8", newline="") as file:
    headers = ["Text", "Author", "Bio-Link"]
    csv_writer = DictWriter(file, fieldnames=headers)
    csv_writer.writeheader()

    for q in all_quotes:
        csv_writer.writerow(q)
