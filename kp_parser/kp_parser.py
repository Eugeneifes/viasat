# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib
import requests
import time
import json
import hashlib
import csv
import os.path
from proxylist import ProxyList
import random
import os

"""

def get_films(file):
    import csv
    with open(file, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)
        for row in reader:
            get_comments(row[1], "comments_db.txt")


def get_comments(code, db):

    if os.path.exists(db):
        with open(db) as json_data:
            comments = json.loads(json_data.read())
    else:
        comments = {}

    print(comments)
    page = "https://www.kinopoisk.ru/film/"+code+"/"
    response = requests.get(page,  proxies=proxies, cookies=cookie)
    print(response.text)


    soup = BeautifulSoup(response.text)
    for elem in soup.find_all("div", class_="reviewItem userReview"):
        text = elem.find("span", class_='_reachbanner_')
        comments["text"] = text.get_text()
        comments["hash"] = hashlib.md5(text.get_text().encode("utf-8")).hexdigest()
        with open('data.txt', 'w') as outfile:
            json.dump(comments, outfile)

"""




def load_comments():
    hash_table = []
    for dir in os.listdir("comments"):
        for file in os.listdir("comments/"+dir):
            with open("comments/"+dir+"/" +file, "r") as text_file:
                hash = hashlib.md5(text_file.read()).hexdigest()
                hash_table.append(hash)
    return hash_table


films = {"Deadpool": "462360", "WarCraft": "277328"}
cookie = {"Cookie": "_ym_uid=148275645871589465; fuid01=5861116a2c1787d3.0L2vkBKNsxSxrfStruCZIoMbzgUovNbeyr4hwjRYcRh-3nmA7tLgXpevj9KapETpIrSxVjibPi9qKwLyJn8AHw4Yh2dpxYhNaPyRBk_4Btj_XI_3HQfIZHLQnW_960bn; yandexuid=8433106741482739582; PHPSESSID=1e64d0364c2e79c3f4f3a1131e505f42; yandex_gid=213; last_visit=2017-03-07+11%3A32%3A12; _ym_isad=2; my_perpages=%5B%5D; noflash=false; user_country=ru"}

hash_table = load_comments()


def get_comments_pages(film_name, code):

    if os.path.isdir("comments/"+film_name):
        if os.listdir("comments/"+film_name) != []:
            page_num = len(os.listdir("comments/"+film_name)) + 1
        else:
            page_num = 1
    else:
        os.mkdir("comments/"+film_name)
        page_num = 1

    page = "https://www.kinopoisk.ru/film/"+code+"/ord/rating/perpage/10/page/"+str(page_num)+"/#list"
    response = requests.get(page, cookies=cookie)
    soup = BeautifulSoup(response.text)
    while soup.find_all("div", class_ = "reviewItem userReview") != []:
        with open("comments/"+film_name+"/"+"page_"+str(page_num), "w") as comments:
            comments.write(response.text.encode("utf-8"))
        page_num += 1
        page = "https://www.kinopoisk.ru/film/" + code + "/ord/rating/perpage/10/page/" + str(page_num) + "/#list"
        response = requests.get(page, cookies=cookie)
        soup = BeautifulSoup(response.text)


def parse_comments(film_name):
    for page in os.listdir("comments/"+film_name):
        with open("comments/"+film_name+"/"+page, "r") as html_page:
            html = html_page.read()
            soup = BeautifulSoup(html)
            comment_blocks = soup.find_all("div", class_="reviewItem userReview")
            for block in comment_blocks:
                comments = block.find("span", class_="_reachbanner_")
                print(comments.text)


#print(hash_table)
#print(len(hash_table))
#get_comments_pages("WarCraft", "277328")
parse_comments("WarCraft")
