from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import database

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

class P2000Message:
    def __init__(self, date, time, region, service, capcodes):
        self.date = date
        self.time = time
        self.region = region
        self.service = service
        self.capcodes = capcodes

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
            # msgCapCodes += capCode.text + "\n"
            msgCapCodes = capCode.text.split(" ")[0]

        msg = P2000Message(time=msgTime, date=msgDate, region=P2000Regions[int(msgRegion)], service=services, capcodes=msgCapCodes)
        P2000Messages.append(msg)
        print('.', end="")
except:
    for message in P2000Messages:
        print(f'\n\t[MESSAGE]\nDate: {message.date}\nTime: {message.time}\nRegion: {message.region}\n{message.service}\n{message.capcodes}')
        database.insertData(message.service, message.capcodes, message.date, message.time, message.region)    
    print("No more messages")
    driver.close()