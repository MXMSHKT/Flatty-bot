import requests
from bs4 import BeautifulSoup
import time
import random
from fake_useragent import UserAgent
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_html(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Mobile Safari/537.36",
        "Accept - encoding": "gzip, deflate, br",
        "cache - control": "max - age = 0"
    }
    req = requests.get(url, headers)
    return req.text.encode(req.encoding)


def get_address(soup):
    try:
        address = soup.find("address").text.strip()
        if "На карте" in address:
            address = address[:address.rfind("На карте")]
        city, district, street, block_number, county = "Не указано" * 5
        city = address.split(",")[0].strip()
        county = address.split(",")[1].strip()
        block_number = address.split(",")[-1].strip()

        for param in address.split(",")[1:-1]:
            if "ул " in param.lower() or "ул." in param.lower() or "улица" in param.lower() or " пер" in param.lower() \
                    or "проезд" in param.lower() or "проспект" in param.lower() or "бульвар" in param.lower():
                street = param.strip()
            elif "район" in param.lower() or "р-н" in param.lower():
                district = param.strip()

        if street.split()[-1].strip().isdigit():
            block_number = street.split()[-1].strip()
            street = " ".join(street.split()[:-1]).strip()

        return city, county, district, street, block_number
    except Exception as e:
        with open("logs.txt", "a", encoding="utf8") as file:
            file.write(str(e) + " cian get_title\n")
    return ["Не указано"] * 5


def get_price(soup):
    try:
        price = soup.find("span", {"itemprop": "price"})
        if price is not None:
            price = price.text.split('₽')[0].strip()

    except Exception as e:
        with open("logs.txt", "a", encoding="utf8") as file:
            file.write(str(e) + " cian get_price\n")
        price = "Не указано"
    return price


def get_photos(url):
    pass


def get_metro(soup):
    name, timing = "Не указано" *2
    return name, timing

def get_description(soup):
    try:
        paragraphs = [x for x in soup.find_all("p") if x.get("class") is not None
                      and len(x.get("class")) == 1 and "description-text--" in x.get("class")[0]]
        description = paragraphs[0].text.strip()
    except Exception as e:
        with open("logs.txt", "a", encoding="utf8") as file:
            file.write(str(e) + " cian get_description\n")
        description = "Не указано"
    return description

def get_date(soup):
    try:
        date = soup.find("div", id="frontend-offer-card").find("main").find_all("div")[4].text.strip()
        tt = date.split()[1]
        if "вчера" in date:
            date = str(datetime.datetime.today() - datetime.timedelta(days=1)).split()[0]
        elif "сегодня" in date:
            date = str(datetime.datetime.today()).split()[0]
        else:
            date = "too old"
    except Exception as e:
        with open("logs.txt", "a", encoding="utf8") as file:
            file.write(str(e) + " cian get_date\n")

        date = "Не указано"
        tt = "Не указано"
    return date, tt


def get_params(soup):
    rooms_number, total_floors, \
        total_area, year, kitchen_area, living_area, floor = ["Не указано"] * 7
    try:
        main_titles = [title.text.strip() for title in soup.find_all("div") if title.get("class") is not None
                       and len(title.get("class")) == 1
                        and "info-title" in title.get("class")[0]]
        main_values = [value.text.strip() for value in soup.find_all("div") if value.get("class") is not None
                       and len(value.get("class")) == 1 and "info-value" in value.get("class")[0]]
        for i in range(len(main_titles)):
            if "Общая" in main_titles[i]:
                total_area = main_values[i]
            elif "Жилая" in main_titles[i]:
                living_area = main_values[i]
            elif "Кухня" in main_titles[i]:
                kitchen_area = main_values[i]
            elif "Построен" in main_titles[i]:
                year = main_values[i]
            elif "Этаж" in main_titles[i]:
                floor = main_values[i].split(" ")[0].strip()
                total_floors = main_values[i].split(" ")[-1].strip()

        rooms_number = soup.find("h1").text.split(",")[0].strip()

    except Exception as e:
        with open("logs.txt", "a", encoding="utf8") as file:
            file.write(str(e) + " cian get_apartment_params\n")
    return total_area, living_area,  rooms_number, total_floors,  year, kitchen_area, floor



def pagination(url,html):
    pass


def get_selemium(url):
    options = webdriver.FirefoxOptions()
    options.set_preference("general.useragent.override",
                           "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Mobile Safari/537.36")
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(url)
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, "lxml")
        city, county, district, street, block_number = get_address(soup)
        print(city, county, district, street, block_number)
        date, dtime = get_date(soup)
        print("Date time- ", date, dtime)
        price = get_price(soup)
        print('price - ', price)
        total_area, living_area,  rooms_number, total_floors,  year, kitchen_area, floor = get_params(soup)
        print(total_area, living_area,  rooms_number, total_floors,  year, kitchen_area, floor)
    except Exception as e:
        with open("logs.txt", "a", encoding="utf8") as file:
            file.write(str(e) + " main\n")
    finally:
        driver.close()
        driver.quit()


def main():
    url = 'https://www.cian.ru/rent/flat/281181077/'
    get_selemium(url)

    #soup = BeautifulSoup(get_selemium(url), "lxml")
    #address = soup.find("address")  # .text.strip()
    #city, district, street, block_number = get_address(soup)
    #print(address)


if __name__ == "__main__":
    main()
