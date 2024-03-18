from test import CryptoNewsScraper
def main():
    print("Scraping crypto potato news...")
    scraper = CryptoNewsScraper()
    news_data = scraper.scrape_news(pages=4)
    if news_data:
        scraper.write_to_csv(news_data)
        print("Crypto news scraped and saved to 'crypto_potato_news.csv'")
    else:
        print("No data scraped")

if __name__ == "__main__":
    main()




