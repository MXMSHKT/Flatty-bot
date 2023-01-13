# -*- coding: utf-8 -*-
from data_parcing import *


def chunker_list(seq, size):
    for pos in range(0, len(seq), size):
        yield seq[pos:pos + size]


def parse(url, pools=5):
    #flat_links = pagination(url, page_limit=100)
    #flat_links = list(set(flat_links))
    #print("all links was found")

    file = open('used_page.txt')
    flat_links = [x.strip() for x in file.readlines() if col.find_one({"_id": int(x.split("/")[-2].strip())}) is None]
    print(len(flat_links))
    for chunk in tqdm(chunker_list(flat_links, pools), total=len(flat_links) // pools):
        tasks = []
        for link in chunk:
            tasks.append(threading.Thread(target=get_data, args=(link,)))
        for task in tasks:
            task.start()
        for task in tasks:
            task.join()
    print("Scraping is completed")


def main():
    url1 = 'https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&region=1&sort=creation_date_desc&type=4&p=1'
    parse(url1)
    #url ='https://www.cian.ru/rent/flat/281695839/'
    #get_data(url)


if __name__ == "__main__":
    main()