from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.p2000Message import P2000Message
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

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.page_load_strategy = "none"

driver = Chrome(options=options)
driver.implicitly_wait(5)
driver.get("https://m.livep2000.nl/")

def tryElement(element, cssSelector):
    try:
        items = element.find_elements(By.CSS_SELECTOR, cssSelector)
        msg = ""
        for item in items:
            msg += item.text + " "
        return msg
    except:
        return ""

content = driver.find_elements(By.CSS_SELECTOR, ".line")
try:
    for element in content:
        msgTime = element.find_element(By.CSS_SELECTOR, ".time").text
        msgDate = element.find_element(By.CSS_SELECTOR, ".date").text
        msgRegion = element.find_element(By.CSS_SELECTOR, ".regio").text

        capCodes = element.find_elements(By.CSS_SELECTOR, ".capcodes")
        services = tryElement(element, ".ambu")
        if len(services) <= 0:
            services = tryElement(element, ".bran")
            if len(services) <= 0:
                services = tryElement(element, ".poli")

        msgCapCodes = ""
        for capCode in capCodes:
            # msgCapCodes += capCode.text + "-"
            msgCapCodes += capCode.text
            break   # database value is only 100 characters

        info = msgCapCodes[8:]

        msg = P2000Message(Tijd=msgTime, 
                           Datum=datetime.strptime(msgDate, "%d-%m-%y"), 
                           Regio=P2000Regions[int(msgRegion)], 
                           Prioriteit=2,
                           ABP=services.split(" ")[0], 
                           Capcode=msgCapCodes.split(" ")[0])
        P2000Messages.append(msg)
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

    db.add_all(P2000Messages)
    db.commit()

    for message in db.query(P2000Message).all():
        print(f'\t[Message]\n{message.Datum}\n{message.Tijd}\n{message.ABP}\n{message.Prioriteit}\n{message.Regio}\n{message.Capcode}\n')

    db.close()

    print("No more messages")
    driver.close()