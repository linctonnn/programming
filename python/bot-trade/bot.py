import requests
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
import time
import random

# --- CONFIGURATION ---
DEFAULT_URL = 'https://coinmarketcap.com/currencies/bitcoin/'
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
]

def scrape_realtime_price(url):
    """Scrape crypto price from CoinMarketCap with improved selectors"""
    try:
        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Try multiple selectors - CoinMarketCap changes these frequently
        selectors = [
            {'class': 'priceValue'},  # Older version
            {'data-testid': 'price-value'},  # Newer version
            {'class': 'sc-f70bb44c-0'},  # Another common class
            {'class': 'sc-1eb5slv-0'},  # Another variant
            {'data-role': 'coin-price'}  # Sometimes used
        ]

        for selector in selectors:
            price_element = soup.find('span', selector)
            if price_element:
                price_text = price_element.get_text()
                # Clean the price string
                price_clean = price_text.replace('$', '').replace(',', '').strip()
                try:
                    return float(price_clean)
                except ValueError:
                    continue

        # If all selectors fail, try more aggressive search
        price_elements = soup.find_all('span')
        for element in price_elements:
            text = element.get_text().strip()
            if text.startswith('$') and ',' in text:
                try:
                    return float(text[1:].replace(',', ''))
                except ValueError:
                    continue

        print("Price element not found. Possible reasons:")
        print("- Website structure changed")
        print("- Anti-bot protection triggered")
        print("- JavaScript-rendered content not visible")
        return None

    except Exception as e:
        print(f"Scraping error: {str(e)}")
        return None

def main():
    print("="*50)
    print("Crypto Price Scraper with Monte Carlo Simulation")
    print("="*50)

    url = input(f"Enter CoinMarketCap URL (default: {DEFAULT_URL}): ") or DEFAULT_URL
    historical_prices = []

    try:
        plt.ion()
        fig, ax = plt.subplots(figsize=(12, 6))

        while True:
            price = scrape_realtime_price(url)
            if price:
                historical_prices.append(price)
                print(f"Current price: ${price:,.2f} | Data points: {len(historical_prices)}")

                # Simple plot of historical data
                ax.clear()
                ax.plot(historical_prices, 'b-', label='Price History')
                ax.set_title("Bitcoin Price History")
                ax.set_xlabel("Time")
                ax.set_ylabel("Price (USD)")
                ax.grid(True)
                plt.pause(0.1)

            time.sleep(60 + random.uniform(-10, 10))  # Randomize delay

    except KeyboardInterrupt:
        print("\nStopping data collection...")
    finally:
        plt.ioff()
        if historical_prices:
            plt.show()
        print("Program ended.")

if __name__ == "__main__":
    main()
