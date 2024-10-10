import random
import time
import streamlit as st
import pandas as pd
from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from src.scraping import scraper
from src.utils import LOCATIONS, getLocation

service = Service(ChromeDriverManager().install())
options = ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
# options.page_load_strategy = 'none'

driver = Chrome(service=service, options=options)
driver.implicitly_wait(0.5)

st.subheader("Empleos Nicaragua")
st.write(
    "Simple aplicación que obtiene ofertas laborales de las 5 primeras páginas del sitio web computrabajo"
)

locationOption = st.selectbox(
    "Seleccione Departamento",
    options=list(LOCATIONS.keys()),
    format_func=getLocation,
)

jobUrl = getLocation(locationOption)

with st.spinner("Cargando datos..."):
    sleepTime = [1, 2, 3, 4, 5]

    data = []
    for i in range(1, 6):
        page = jobUrl + "?p={i}"

        # avoid ban :v
        randomSleepTime = random.choice(sleepTime)
        print(f"Page {i}, esperando {randomSleepTime} segundos")
        time.sleep(randomSleepTime)

        row = scraper(driver, page)
        data.append(row)

print('\n')
dataFlatten = [item for row in data for item in row]
columns = [["cargo", "empresa", "web", "publicado"]]

if len(dataFlatten):
    df = pd.DataFrame(dataFlatten, columns=columns[0])
    st.markdown(df.to_html(escape=False), unsafe_allow_html=True)
else:
    st.write("No se encontraron datos")

driver.quit()