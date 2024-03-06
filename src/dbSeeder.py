""" Database seeder

Populates the P2000 database with data.
Can also create a local database by setting the seedLocal variable to True.

This script makes use of the selenium driver to scrape the 
https://m.livep2000.nl/ website for p2000 messages.
"""
# from webdriver_manager.chrome import ChromeDriverManager
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
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

options = webdriver.ChromeOptions()
options.page_load_strategy = 'none'
options.add_argument("--headless") # Voert chrome uit in headless modus
options.page_load_strategy = "none"

# Initialiseren van de Chrome driver
driver = Chrome(options=options)
 
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

Session = SessionLocal()
print(Session.query(ABP.abp_naam).all())

def get_abp(abp_name):
    abp = Session.query(ABP.abp_id).filter(ABP.abp_naam.like(f'{abp_name}%')).first()
    output = abp
    abp = output[0]
    return abp



def get_prio():
     return random.randint(1, 3)

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
        services = services[:4].lower()
        

        regio_id = int(msgRegion)
        abp_id = get_abp(services)
        prio = get_prio()
        

        melding = Meldingen(
            regio_id=regio_id,
            abp_id=abp_id,
            prioriteit=prio,
            datum=datetime.strptime(msgDate,"%d-%m-%y"),
            tijd=msgTime
        )
        Session.add(melding)
        print("Added message - Regio ID:", regio_id, "ABP ID:", abp_id, "Date:", msgDate, "Time:", msgTime)
         
        print('.', end="")
        Session.commit()
except Exception as e:
    print("An error occurred:", str(e))
    db = None
    if seedLocal:
        localEngine = create_engine("sqlite:///test_messages.db")
        Base.metadata.create_all(bind=localEngine)
        localDbSession = sessionmaker(autocommit=False, autoflush=False, bind=localEngine)
        db = localDbSession()
    else:
        db = SessionLocal()

    Session.close()

    print("No more messages")
    driver.close()