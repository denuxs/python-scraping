from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()

API_URL = os.getenv("API_URL")
COMPANY_SKIP = os.getenv("COMPANY_SKIP")

def scraper(driver, pageUrl):
    driver.get(pageUrl)
    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")

    articles = soup.find_all("article")

    companySkip = COMPANY_SKIP.split(",")
    data = []
    for article in articles:
        link = article.h2.a.get("href")
        title = article.h2.a.get_text(strip=True)

        paragraphes = article.find_all("p")
        company = paragraphes[0]

        if company.find("a"):
            company = company.a.get_text(strip=True)
        else:
            company = company.get_text(strip=True)

        if company not in companySkip:
            published = paragraphes[-2].get_text(strip=True)

            link = f'<a href="{API_URL}/{link}" target="_blank" >Oferta</a>'
            data.append([title, company, link, published])

    return data
