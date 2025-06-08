import requests
from bs4 import BeautifulSoup
import csv
import time

# User-Agent to mimic a browser visit
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# Example: Search for "laptop" on Amazon
URL = "https://www.amazon.in/s?k=laptop"

response = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(response.content, "html.parser")

# Find all product containers
products = soup.find_all("div", {"data-component-type": "s-search-result"})

with open("amazon_products.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Price", "Rating"])
    for product in products:
        # Product Name
        name_tag = product.h2.a
        name = name_tag.text.strip() if name_tag else "N/A"

        # Price
        price_whole = product.find("span", class_="a-price-whole")
        price_fraction = product.find("span", class_="a-price-fraction")
        if price_whole and price_fraction:
            price = f"{price_whole.text.strip()}.{price_fraction.text.strip()}"
        else:
            price = "N/A"

        # Rating
        rating_tag = product.find("span", class_="a-icon-alt")
        rating = rating_tag.text.split(' ')[0] if rating_tag else "N/A"

        writer.writerow([name, price, rating])

print("Scraping complete. Data saved to amazon_products.csv.")