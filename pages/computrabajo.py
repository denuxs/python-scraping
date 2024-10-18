import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from src.scraper import Scraper

load_dotenv()

API_URL = os.getenv("COMPUTRABAJO_URL")
COMPANY_SKIP = os.getenv("COMPANY_SKIP")
USE_SELENIUM = os.getenv("USE_SELENIUM")

LOCATIONS = {
    1: "/empleos-en-matagalpa",
    2: "/empleos-en-managua",
    3: "/empleos-en-leon",
    4: "/empleos-en-esteli",
    5: "/empleos-en-jinotega",
    6: "/empleos-en-masaya",
    7: "/empleos-en-granada",
}


def getLocation(option):
    location = LOCATIONS[option]
    return API_URL + location


def getJobsScraper(html):
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

scraper = Scraper()
html = scraper.fetch_page(jobUrl, use_header=True)

data = []
row = getJobsScraper(html)
data.append(row)

with st.spinner("Cargando datos..."):
    for i in range(2, 6):
        page = jobUrl + f"?p={i}"

        html = scraper.fetch_page(page, use_header=True)

        row = getJobsScraper(html)
        data.append(row)

scraper.close()

print("\n")
dataFlatten = [item for row in data for item in row]

columns = [["cargo", "empresa", "web", "publicado"]]

if len(dataFlatten):
    df = pd.DataFrame(dataFlatten, columns=columns[0])
    st.markdown(df.to_html(escape=False), unsafe_allow_html=True)
else:
    st.write("No se encontraron datos")
