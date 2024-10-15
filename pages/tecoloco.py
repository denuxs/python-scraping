import random
import time
from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

API_URL = os.getenv("TECOLOCO_URL")
PAGE_URL = API_URL + "/empleo-informatica-internet"

COMPANY_SKIP = os.getenv("COMPANY_SKIP")

service = Service(ChromeDriverManager().install())
options = ChromeOptions()
options.add_argument("--headless=new")

selenium = Chrome(service=service, options=options)
selenium.implicitly_wait(0.5)


def getPageSource(page):
    selenium.get(page)
    html = selenium.page_source

    return BeautifulSoup(html, "html.parser")


def runScraper(html):
    jobs = html.find_all(class_="module job-result")

    companySkip = COMPANY_SKIP.split(",")
    companySkip = list(map(lambda x: x.strip(), companySkip))

    data = []
    for job in jobs:
        title = job.find("h2").get_text(strip=True)
        link = job.find("h2").a.get("href")

        page = API_URL + link
        link = f'<a href="{page}" target="_blank">Oferta</a>'

        detail = job.find(class_="job-overview")
        company = detail.find(class_="name").get_text(strip=True)
        expires = detail.find(class_="updated-time").get_text(strip=True)
        city = detail.find(class_="location").get_text(strip=True)

        if company not in companySkip:
            data.append([title, company, city, link, expires])

    return data


st.subheader("Tecoloco Empleos")

html = getPageSource(PAGE_URL)

pagination = html.find(id="pagination")
pages = pagination.find_all("li")

data = []
row = runScraper(html)
data.append(row)

with st.spinner("Cargando datos..."):
    if len(pages) > 1:
        sleepTime = [1, 2, 3, 4, 5]

        for i in pages[1:-1]:
            page = PAGE_URL + "?Page={i}"

            html = getPageSource(page)

            # avoid ban :v
            randomSleepTime = random.choice(sleepTime)
            print(f"Page {i}, esperando {randomSleepTime} segundos")
            time.sleep(randomSleepTime)

            row = runScraper(html)
            data.append(row)

print("\n")
dataFlatten = [item for row in data for item in row]

columns = [["cargo", "empresa", "ciudad", "web", "expira"]]

if len(dataFlatten):
    df = pd.DataFrame(dataFlatten, columns=columns[0])
    st.markdown(df.to_html(escape=False), unsafe_allow_html=True)
else:
    st.write("No se encontraron datos")

selenium.quit()
