# coding=utf8
import requests
from bs4 import BeautifulSoup
import time
import os
from tqdm import tqdm
import random
import dateparser
from fake_useragent import UserAgent
import datetime
import locale
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from db import *


def get_address(soup):
    district, street = "Не указано", "Не указано"
    try:
        address = soup.find("address").text.strip()
        if "На карте" in address:
            address = address[:address.rfind("На карте")]
        city = address.split(",")[0].strip()
        county = address.split(",")[1].strip()
        block_number = address.split(",")[-1].strip()

        for param in address.split(",")[1:-1]:
            if "ул " in param.lower() or "ул." in param.lower() or "улица" in param.lower() or " пер" in param.lower() \
                    or "просп" in param.lower() or "проезд" in param.lower() or "проспект" in param.lower() \
                    or "бульвар" in param.lower() or "наб" in param.lower():
                street = param.strip()
                if street.split()[-1].strip().isdigit():
                    block_number = street.split()[-1].strip()
                    street = " ".join(street.split()[:-1]).strip()

            elif "район" in param.lower() or "р-н" in param.lower():
                district = param.strip()
        return city, county, district, street, block_number
    except Exception as e:
        with open("logs.txt", "a", encoding="utf8") as file:
            file.write(str(e) + " cian get_title\n")
        return ["Не указано"] * 5


def get_price(soup):
    price = "Не указано"
    try:
        price = soup.find("span", {"itemprop": "price"})
        if price is not None:
            price = int(price.text.replace('\xa0', '').split('₽')[0].strip())

    except Exception as e:
        with open("logs.txt", "a", encoding="utf8") as file:
            file.write(str(e) + " cian get_price\n")
    return price


def get_photos(soup, cian_id):
    photos_links = "Не указано"
    try:
        photos_links = soup.find_all("img", {"data-name": "ThumbComponent"})
        photos_links = [x['src'] for x in photos_links]

    except Exception as e:
        with open("logs.txt", "a", encoding="utf8") as file:
            file.write(str(e) + " - can't find photo link\n")

    try:
        pathname = "photos" + "\\" + cian_id
        for photo in photos_links:
            download(photo, pathname)
    except Exception as e:
        with open("logs.txt", "a", encoding="utf8") as file:
            file.write(str(e) + " - can't download photo\n")
    return photos_links


def download(url, pathname):
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    response = requests.get(url, stream=True)
    filename = os.path.join(pathname, url.split("/")[-1])
    with open(filename, "wb") as f:
        for data in response:
            f.write(data)


def get_metro(soup):
    underground = "Не указано"
    try:
        underground = [x.text.strip() for x in soup.find_all("li") if x.get("class") is not None \
                       and "underground" in str(x.get("class"))]
    except Exception as e:
        with open("logs.txt", "a", encoding="utf8") as file:
            file.write(str(e) + " cian get_metro\n")
    return underground


def get_description(soup):
    description = "Не указано"
    try:
        paragraphs = [x for x in soup.find_all("p") if x.get("class") is not None
                      and len(x.get("class")) == 1 and "description-text--" in x.get("class")[0]]
        description = paragraphs[0].text.strip()
    except Exception as e:
        with open("logs.txt", "a", encoding="utf8") as file:
            file.write(str(e) + " cian get_description\n")
    return description


def get_date(soup):
    date = "Не указано"
    try:
        date = soup.find("div", id="frontend-offer-card").find("main").find_all("div")[4].text.strip()
        timme = date.split(",")[-1].strip()
        date = str(dateparser.parse(date)).split(" ")[0] + ", " + timme
    except Exception as e:
        with open("logs.txt", "a", encoding="utf8") as file:
            file.write(str(e) + " cian get_date\n")

    return date


def get_params(soup):
    rooms_number, total_floors, \
        total_area, year, kitchen_area, living_area, floor = ["Не указано"] * 7
    try:
        main_titles = [title.text.strip() for title in soup.find_all("div") if title.get("class") is not None
                       and len(title.get("class")) == 1
                       and "info-title" in title.get("class")[0]]
        main_values = [value.text.replace('\xa0', ' ').strip() for value in soup.find_all("div") if
                       value.get("class") is not None
                       and len(value.get("class")) == 1 and "info-value" in value.get("class")[0]]

        for i in range(len(main_titles)):
            if "Общая" in main_titles[i]:
                total = main_values[i].replace(',', '.')
                total_area = float(total.split(" ")[0].strip())
            elif "Жилая" in main_titles[i]:
                living = main_values[i].replace(',', '.')
                living_area = float(living.split(" ")[0].strip())
            elif "Кухня" in main_titles[i]:
                kitchen = main_values[i].replace(',', '.')
                kitchen_area = float(kitchen.split(" ")[0].strip())
            elif "Построен" in main_titles[i]:
                year = int(main_values[i])
            elif "Этаж" in main_titles[i]:
                floor = int(main_values[i].split(" ")[0].strip())
                total_floors = int(main_values[i].split(" ")[-1].strip())

        rooms_number = soup.find("h1").text.split(",")[0].strip()

    except Exception as e:
        with open("logs.txt", "a", encoding="utf8") as file:
            file.write(str(e) + " cian get_apartment_params\n")
    return total_area, living_area, rooms_number, total_floors, year, kitchen_area, floor


def pagination(url, page_limit=100):
    options = webdriver.FirefoxOptions()
    options.set_preference("general.useragent.override",
                           "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, "
                           "like Gecko) Chrome/86.0.4240.183 Mobile Safari/537.36")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.delete_all_cookies()
    page = 1
    Page_off = False
    flat_links = []
    try:
        while not Page_off:
            print("page", page)
            page_url = url[:url.rfind("=") + 1] + str(page)
            print(page_url)
            driver.get(page_url)
            time.sleep(5)
            soup = BeautifulSoup(driver.page_source, "lxml")

            links = soup.find_all("article", {"data-name": "CardComponent"})
            links = [x.find("a").get("href") for x in links]
            print(links)
            if not links:
                with open("unused_page.txt", "a", encoding="utf8") as file:
                    file.write(page_url + "\n")
                page -= 1

            if links:
                activepage = [x.text.strip() for x in soup.find("div", {"data-name": "Pagination"}).find_all("li") if
                              x.get("class") is not None and len(x.get("class")) == 2]
                print("activepage", activepage)
                for i in links:
                    cian_id = int(url.split("/")[-2].strip())
                    if i not in flat_links and col.find_one({"_id": cian_id}) is None:
                        flat_links += links
                    else:
                        print("Flat - ", cian_id, " was processed")
                    if col.find_one({"_id": cian_id}):
                        print("Flat - ", cian_id, " in DB")
                        Page_off = True
                        continue
                if page != int(activepage[0]):
                    print("page != activepage")
                    Page_off = True

            if page == page_limit:
                Page_off = True
            page += 1

    except Exception as e:
        with open("logs.txt", "a", encoding="utf8") as file:
            file.write(str(e) + " wrongs with pagination\n")
    finally:
        driver.close()
        driver.quit()

    for i in flat_links:
        with open("used_page.txt", "a", encoding="utf8") as file:
            file.write(i + "\n")
    return flat_links


def get_data(url):
    options = webdriver.FirefoxOptions()
    options.set_preference("general.useragent.override",
                           "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, "
                           "like Gecko) Chrome/86.0.4240.183 Mobile Safari/537.36")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.delete_all_cookies()
    try:
        driver.get(url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, "lxml")
        city, county, district, street, block_number = get_address(soup)
        date = get_date(soup)
        price = get_price(soup)
        total_area, living_area, rooms_number, total_floors, year, kitchen_area, floor = get_params(soup)
        description = get_description(soup)
        Metro = get_metro(soup)
        get_photos(soup, url.split("/")[-2].strip())
        flat = {"Link": url,
                "_id": int(url.split("/")[-2].strip()),
                "Date": date.split(",")[0].strip(),
                "Time": date.split(",")[-1].strip(),
                "Address": {"City": city,
                            "County": county,
                            "District": district,
                            "Street": street,
                            "BlockNumber": block_number},
                "Metro": Metro,
                "FlatParams": {
                    "Total_area": total_area,
                    "Living_area": living_area,
                    "Rooms_number": rooms_number,
                    "Total_floors": total_floors,
                    "Year": year,
                    "Kitchen_area": kitchen_area,
                    "floor": floor},
                "Price": price,
                "Description": description}
        x = col.insert_one(flat)
    except Exception as e:
        with open("logs.txt", "a", encoding="utf8") as file:
            file.write(str(e) + " main\n")
    finally:
        driver.close()
        driver.quit()

