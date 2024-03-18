import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, date

class CryptoNewsScraper:
    def scrape_news(self, pages=8):
        base_url = "https://cryptopotato.com/category/crypto-news/"
        news_data = []

        for page in range(1, pages + 1):
            url = f"{base_url}?page={page}"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            # Find all news articles on the page
            articles = soup.find_all("article")

            for article in articles:
                # Extract the title and link of each news article
                title_element = article.find('h3', class_='media-heading')
                link = title_element.find('a')['href'] if title_element.find('a') else "N/A"
                title = title_element.text.strip() if title_element else "N/A"

                # Extract additional information
                time_element = article.find('div', class_='entry-meta').find('span', class_='entry-time').text.strip()

                # Get the content of the news article
                content = self.get_article_content(link)

                news_data.append({
                    "Title": title,
                    "Time": time_element,
                    "Content": content
                })

        return news_data

    def get_article_content(self, link):
        article_response = requests.get(link)
        article_soup = BeautifulSoup(article_response.text, "html.parser")
        content_element = article_soup.find("div", class_="entry-content col-sm-11")
        content = content_element.get_text(strip=True) if content_element else "N/A"
        return content

    def write_to_csv(self, news_data, filename="crypto_potato_news"):
        file_date = date.today().strftime("%Y-%m-%d")
        filename_with_date = f"{filename}_{file_date}.csv"

        with open(filename_with_date, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["Time", "Date", "Title", "Content"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            # Iterate over news data and write to CSV
            for news_item in news_data:
                # Extract time string
                time_str = news_item["Time"]
                # Extract date string
                date_str = date.today().strftime("%Y-%m-%d")
                # Write the updated news item to CSV
                writer.writerow({
                    "Time": time_str,
                    "Date": date_str,
                    "Title": news_item["Title"],
                    "Content": news_item["Content"]
                })
