# -*- coding: utf-8 -*-
from data_parcing import *


def parse(category_url):
    completed = False
    page = 1
    while not completed:
        url = category_url[:category_url.rfind("=") + 1] + str(page)
        completed = pagination(page, get_selemium(url))
        page += 1

def main():
    url = " "
    parse(url)

if __name__ == "__main__":
    main()