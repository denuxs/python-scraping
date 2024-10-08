import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")

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
