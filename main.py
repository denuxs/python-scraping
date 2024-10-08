import random
import time
import streamlit as st
import pandas as pd

from scraping import fetchJobData
from utils import LOCATIONS, getLocation

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
        page = f"{jobUrl}?p={i}"

        # avoid ban :v
        randomSleepTime = random.choice(sleepTime)
        print(f"Esperando por {randomSleepTime} segundos")
        time.sleep(randomSleepTime)

        row = fetchJobData(page)
        data.append(row)

    dataFlatten = [item for row in data for item in row]

if len(dataFlatten):
    df = pd.DataFrame.from_dict(dataFlatten)
    st.markdown(df.to_html(render_links=True, escape=False), unsafe_allow_html=True)
else:
    st.write("No se encontraron datos")
