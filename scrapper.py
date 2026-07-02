from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
import random
import csv

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
]


def scrap_html(url, selector='a[href*="/item/"]'):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_extra_http_headers({"User-Agent": random.choice(user_agents)})
        page.goto(url)
        page.wait_for_load_state('networkidle')  
        links = page.eval_on_selector_all(
            selector,
            '''els => els.map(e=>({
            url: e.href,
            name: e.getAttribute("aria-label"),
            price: e.querySelector("[aria-label='Item price']")?.innerText || "N/A"
            }))'''
        )
        browser.close()
        seen = set()
        result = []
        for link in links:
            if link["url"] not in seen:
                seen.add(link["url"])
                result.append(link)
        return result  

def create_csv(items):
    with open("scrapped_prices.csv","w",newline='',encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["URL","Name","Price"])
        for item in items:
            writer.writerow([item["url"],item["name"],item["price"]])
        return


def main():
    try:
        url = input("Enter a URL: ")
        response = scrap_html(url)
        create_csv(response)
    except Exception as e:
        print(f"Error: {e}")
    return


if __name__ == "__main__":
    main()