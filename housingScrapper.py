import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd

from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdrivermanager.chrome import ChromeDriverManager
import geopandas as gpd

def housingScrape(area_name):
    pricing = []
    yearlyChangeData = []
    df = {
        "priceIndex" : pricing,
        "yearlyChangeIndex" : yearlyChangeData
    }
    #creating/using http header because otherwise zolo won't connect
    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    )
    headers = {"User-Agent": user_agent}

    url = f"https://www.zolo.ca/toronto-real-estate/{area_name}/trends"
    # url = "https://www.indeed.ca"
    response = get(url,headers=headers)
    if (response.status_code != 200):
        print(f"Can't connect to {url}")
        price = "0.01"
        yearlyChange = "0.01"
        price = float(price)
        yearlyChange = float(yearlyChange)
        pricing.append(price)
        yearlyChangeData.append(yearlyChange)
    else:
        print(f"{area_name}")
        soup = BeautifulSoup(response.text, "html.parser")
        parent_div = soup.find("div", class_="tab-content xs-overflow-hidden xs-pt2 xs-col-12")
        child_div = parent_div.find_all("div", class_="card-value")
        #finding the price
        price_div = parent_div.find("div", class_="card-value").get_text()
        #finding the yearly change
        yearlyChange = child_div[3].get_text()[:-1]
        #if the page area does not match on website
        if yearlyChange == "" or yearlyChange == " " or yearlyChange is None:
            yearlyChange = 0.01
            price = 0.01
        else:
            #if it is below a million
            if price_div[-1] == "K":
                price = price_div[1:-1]
                price = float(price)
                price /= 1000
                # pricing.append(price)
                # yearlyChangeData.append(yearlyChange)
            else:
                price = price_div[1:-1]
                price = float(price)
                # pricing.append(price)
                # yearlyChangeData.append(yearlyChange)
        yearlyChange = float(yearlyChange)
        pricing.append(price)
        yearlyChangeData.append(yearlyChange)
    return df

def extractingAreas():
    areaNames = []
    gdf = gpd.read_file("toronto_crs84.geojson")
    # print(gdf.AREA_NAME.head())
    for i in range(gdf.AREA_NAME.count()):
        area = gdf.AREA_NAME[i]
        if "\n" in area:
            trimmedArea = "N/A"
        else:
            trimmed = area.split("(")
            trimmedArea = trimmed[0]
            trimmedArea = trimmedArea[:-1]
            trimmedArea = trimmedArea.replace(" ", "-")
        areaNames.append(trimmedArea)
    #saving to file
    file = open("housingData.csv", "w")
    file.write("Area Name\n")
    for area in areaNames:
        file.write(f"{area}\n")
    file.close()

def createHousingData():
    df = pd.read_csv("housingData.csv")
    pricingList = []
    yearlyChangeList = []
    for area in df["Area Name"]:
        result = housingScrape(area)
        price = result["priceIndex"]
        yearlyChange = result["yearlyChangeIndex"]
        pricingList.append(price)
        yearlyChangeList.append(yearlyChange)
    df["Price"] = pricingList
    df["Yearly Change"] = yearlyChangeList

    df.to_csv("final_housingData2.csv")


# print(housingScrape("Not-Available"))
# print(housingScrape("Thistletown-Beaumonde-Heights"))
# print(housingScrape("danforth"))

