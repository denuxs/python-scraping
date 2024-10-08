from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv

load_dotenv()

requestHeaders = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "3600",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
}

API_URL = os.getenv("API_URL")
COMPANY_SKIP = os.getenv("COMPANY_SKIP")


def fetchJobData(page):
    response = requests.get(page, headers=requestHeaders)
    # print(response.status_code)

    soup = BeautifulSoup(response.content, "html.parser")

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

            item = {}
            item["cargo"] = title
            item["empresa"] = company

            link = f'<a href="{API_URL}/{link}" target="_blank" >Oferta</a>'
            item["sitio web"] = link
            item["publicado"] = published
            data.append(item)

    return data
