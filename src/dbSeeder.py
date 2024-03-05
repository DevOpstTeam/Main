""" Database seeder

Populates the P2000 database with data.
Can also create a local database by setting the seedLocal variable to True.

This script makes use of the selenium driver to scrape the 
https://m.livep2000.nl/ website for p2000 messages.
"""
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.p2000Message import Regio,ABP,Meldingen
from schemas.p2000Message import P2000MessageCreate, P2000MessageBase, P2000Message
from models.base import Base
from alchemyDatabase import SessionLocal
from datetime import datetime

seedLocal = False

P2000Regions = {1: "Groningen",
           2: "Friesland",
           3: "Drenthe",
           4: "Ijsselland",
           5: "Twente",
           6: "Noord en Oost Gelderland",
           7: "Gelderland Midden",
           8: "Gelderland Zuid",
           9: "Utrecht",
           10: "Noord-Holland Noord",
           11: "Zaanstreek-Waterland",
           12: "Kennemerland",
           13: "Amsterdam-Amstelland",
           14: "Gooi en Vechtstreek",
           15: "Haaglanden",
           16: "Hollands Midden",
           17: "Rotterdam Rijnmond",
           18: "Zuid-Holland",
           19: "Zeeland",
           20: "Midden- en West-Brabant",
           21: "Brabant Noord",
           22: "Brabant Zuid en Oost",
           23: "Limburg Noord",
           24: "Limburg Zuid",
           25: "Flevoland"}

P2000Messages = list()

os.environ['WDM_LOCAL'] = '1'
os.environ['WDM_CACHE_DIR'] = '/tmp/.wdm'
options = FirefoxOptions()
options.add_argument("--headless")  # Voert Firefox uit in headless modus
options.add_argument("--disable-gpu")  # Deze optie is soms nodig voor Firefox in headless modus
options.add_argument("--no-sandbox")  # Deze optie wordt aanbevolen voor het uitvoeren van Firefox in container-omgevingen
options.add_argument("--disable-dev-shm-usage")
# Firefox heeft geen direct equivalent van page_load_strategy 'none', dus die lijn wordt weggelaten

# Initialiseren van de Firefox driver met de bovenstaande opties
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

# Stel een impliciete wachttijd in
driver.implicitly_wait(5)

# Ga naar de website
driver.get("https://m.livep2000.nl/")



def tryElement(element, cssSelector):
    """Try to search an html element for anything that matches the CSS Selector.

    Parameters:
    element: the html element to search.
    cssSelector: CSS selector to look for in the given element.

    Returns:
    str: text from any items matching the CSS selector, separated by spaces.
    """
    try:
        items = element.find_elements(By.CSS_SELECTOR, cssSelector)
        msg = ""
        for item in items:
            msg += item.text + " "
        return msg
    except:
        return ""

content = driver.find_elements(By.CSS_SELECTOR, ".line")

def get_or_create_region(session, region_name):
    region = session.query(Regio).filter(Regio.regio_naam == region_name).first()
    if not region:
        region = Regio(regio_naam=region_name)
        session.add(region)
        session.commit()
    return region.regio_id

def get_or_create_abp(session, abp_name):
    abp = session.query(ABP).filter(ABP.abp_naam == abp_name).first()
    if not abp:
        abp = ABP(abp_naam=abp_name)
        session.add(abp)
        session.commit()
    return abp.abp_id

try:
    content = driver.find_elements(By.CSS_SELECTOR, ".line")
    for element in content:
        msgTime = element.find_element(By.CSS_SELECTOR, ".time").text
        msgDate = element.find_element(By.CSS_SELECTOR, ".date").text
        msgRegion = element.find_element(By.CSS_SELECTOR, ".regio").text

        services = tryElement(element, ".ambu")
        if len(services) <= 0:
            services = tryElement(element, ".bran")
            if len(services) <= 0:
                services = tryElement(element, ".poli")

        regio_id = get_or_create_region(session, msgRegion)
        abp_id = get_or_create_abp(session, info)

        melding = Meldingen(
            regio_id=regio_id,
            abp_id=abp_id,
            prioriteit=2,
            datum=msgDate,
            tijd=msgTime
        )
        print('.', end="")
except:
    # At some point, selenium just fails for this website (because the website auto updates)
    db = None
    if seedLocal:
        localEngine = create_engine("sqlite:///test_messages.db")
        Base.metadata.create_all(bind=localEngine)
        localDbSession = sessionmaker(autocommit=False, autoflush=False, bind=localEngine)
        db = localDbSession()
    else:
        db = SessionLocal()

    db.add(melding)
    db.commit()

    for message in db.query().all():
        print(f'\t[Message]\n{message.Datum}\n{message.Tijd}\n{message.ABP}\n{message.Prioriteit}\n{message.Regio}')

    db.close()

    print("No more messages")
    driver.close()