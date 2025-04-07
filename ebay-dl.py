import argparse
import requests
from bs4 import BeautifulSoup
import json
import re

def parse_arguments():
    parser = argparse.ArgumentParser(description="Scrape eBay search results.")
    parser.add_argument("search_term", type=str, help="Search term to query on eBay.")
    return parser.parse_args()

def fetch_search_results(search_term):
    url = f"https://www.ebay.com/sch/i.html?_nkw={search_term}"
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_item_details(item):
    name = item.find("div", class_="s-item__title")
    name = name.text if name else None

    price = item.find("span", class_="s-item__price")
    if price:
        price_match = re.search(r"\d+\.\d{2}", price.text)
        price = int(float(price_match.group()) * 100) if price_match else None
    else:
        price = None

    status = item.find("span", class_="SECONDARY_INFO")
    status = status.text if status else None

    shipping = item.find("span", class_="s-item__shipping")
    if shipping:
        if "Free shipping" in shipping.text:
            shipping = 0
        else:
            shipping_match = re.search(r"\d+\.\d{2}", shipping.text)
            shipping = int(float(shipping_match.group()) * 100) if shipping_match else None
    else:
        shipping = None

    free_returns = item.find("span", class_="s-item__free-returns")
    free_returns = bool(free_returns)

    items_sold = item.find("span", class_="s-item__quantitySold")
    if items_sold:
        sold_match = re.search(r"(\d+)", items_sold.text.replace(",", ""))
        items_sold = int(sold_match.group()) if sold_match else None
    else:
        items_sold = None

    return {
        "name": name,
        "price": price,
        "status": status,
        "shipping": shipping,
        "free_returns": free_returns,
        "items_sold": items_sold
    }

def extract_items(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    items = soup.find_all("li", class_="s-item", limit=12)
    return [parse_item_details(item) for item in items[2:]]

def save_to_json(data, search_term):
    filename = f"{search_term}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def main():
    args = parse_arguments()
    search_term = args.search_term
    html_content = fetch_search_results(search_term)
    items = extract_items(html_content)
    save_to_json(items, search_term)

if __name__ == "__main__":
    main()





"""
 # Simulate downloading the first 10 results
    for i in range(1, 11):  # Simulate 10 results
        url = f"https://www.ebay.com/sch/i.html?_nkw={search_term}&_pgn={i}"
        print(f"Downloading page {i}: {url}")
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Page {i} downloaded successfully.")
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract item titles
            items = soup.find_all("div", class_="s-item__title")
            if items:
                print(f"Items found on page {i}:")
                for item in items:
                    print(f"- {item.get_text()}")
            else:
                print(f"No items found on page {i}.")
        else:
            print(f"Failed to download page {i}. Status code: {response.status_code}")

"""