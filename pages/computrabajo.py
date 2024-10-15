import random
import time
import streamlit as st
import pandas as pd
from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import sys
import requests

load_dotenv()

API_URL = os.getenv("COMPUTRABAJO_URL")
COMPANY_SKIP = os.getenv("COMPANY_SKIP")
USE_SELENIUM = os.getenv("USE_SELENIUM")

# USER_AGENT = [
#     "Mozilla/5.0 (Linux; Android 4.4.4; [HM NOTE|NOTE-III|NOTE2 1LTET) AppleWebKit/537.39 (KHTML, like Gecko)  Chrome/53.0.2111.335 Mobile Safari/536.6"
#     "Mozilla / 5.0 (compatible; MSIE 8.0; Windows; U; Windows NT 6.2; x64; en-US Trident / 4.0)"
#     "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0_8; like Mac OS X) AppleWebKit/536.13 (KHTML, like Gecko)  Chrome/50.0.2440.333 Mobile Safari/600.1"
#     "Mozilla/5.0 (iPod; CPU iPod OS 11_1_7; like Mac OS X) AppleWebKit/603.49 (KHTML, like Gecko)  Chrome/51.0.1709.273 Mobile Safari/533.6"
# ]

USER_AGENT = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "3600",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
}

LOCATIONS = {
    1: "/empleos-en-matagalpa",
    2: "/empleos-en-managua",
    3: "/empleos-en-leon",
    4: "/empleos-en-esteli",
    5: "/empleos-en-jinotega",
    6: "/empleos-en-masaya",
    7: "/empleos-en-granada",
}

if USE_SELENIUM == "True":
    service = Service(ChromeDriverManager().install())
    options = ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--user-agent=%s" % random.choice(USER_AGENT))
    # options.page_load_strategy = 'none'

    selenium = Chrome(service=service, options=options)
    selenium.implicitly_wait(0.5)


def getLocation(option):
    location = LOCATIONS[option]
    return API_URL + location


def getPageSource(page):
    html = None
    if USE_SELENIUM == "True":
        selenium.get(page)
        html = selenium.page_source
    else:
        response = requests.get(page, headers=USER_AGENT)
        # print(response.status_code)
        html = response.content

    return BeautifulSoup(html, "html.parser")


def runScraper(html):
    articles = html.find_all("article")

    companySkip = COMPANY_SKIP.split(",")
    companySkip = list(map(lambda x: x.strip(), companySkip))

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


st.subheader("Computrabajo Empleos")

locationOption = st.selectbox(
    "Seleccione Departamento",
    options=list(LOCATIONS.keys()),
    format_func=getLocation,
)

jobUrl = getLocation(locationOption)

data = []
with st.spinner("Cargando datos..."):
    sleepTime = [1, 2, 3, 4, 5]

    for i in range(2, 6):
        page = jobUrl + "?p={i}"

        html = getPageSource(page)

        # avoid ban :v
        randomSleepTime = random.choice(sleepTime)
        print(f"Page {i}, esperando {randomSleepTime} segundos")
        time.sleep(randomSleepTime)

        row = runScraper(html)
        data.append(row)

print("\n")
dataFlatten = [item for row in data for item in row]

columns = [["cargo", "empresa", "web", "publicado"]]

if len(dataFlatten):
    df = pd.DataFrame(dataFlatten, columns=columns[0])
    st.markdown(df.to_html(escape=False), unsafe_allow_html=True)
else:
    st.write("No se encontraron datos")

if USE_SELENIUM == "True":
    selenium.quit()
