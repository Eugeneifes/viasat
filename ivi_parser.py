#-*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
import urllib2
import re
import sqlite3 as db
from pymongo import MongoClient




"""
conn = db.connect('ivi.db')
cursor = conn.cursor()
"""


'''SQLite connection'''
"""
cursor.execute("drop table films")
cursor.execute("drop table series")
cursor.execute("create table films(title text, model text)")
cursor.execute("create table series(title text, model text)")
"""


'''Mongodb connection'''
conn = MongoClient("172.20.2.29", 27017)
print conn.server_info()
db = conn.ivi
coll = db['films']



"""



'''Parsing ivi'''
menu = {}

menu["Фильмы"] = "https://www.ivi.ru/movies"
menu["Новинки"] = "https://www.ivi.ru/new"
menu["Сериалы"] = "http://www.ivi.ru/series"
#menu["Скоро в кинотеатрах"] = "https://www.ivi.ru/new/coming-soon"

def get_new():
    page = urllib2.urlopen(menu["Новинки"])
    soup = BeautifulSoup(page.read())

    elems = soup.findAll("a", {"class": re.compile('^item-content-wrapper*')})
    for i, elem in enumerate(elems):
        tags = elem.findAll("span")
        business_type = tags[0].get("data-caption")
        film = tags[2].span.getText()
        cursor.execute("insert into films values(" +film+"," +business_type+")")

"""
def get_films():
    pagenum=1
    films_c=0
    while pagenum<=208:
        print pagenum
        try:
            page = urllib2.urlopen(menu["Фильмы"]+"/page"+str(pagenum))
            soup = BeautifulSoup(page.read())

            elems = soup.findAll("a", {"class": re.compile('^item-content-wrapper*')})
            for i, elem in enumerate(elems):
                films_c+=1
                tags = elem.findAll("span")
                model = tags[0].get("data-caption")
                film = tags[2].span.getText()
                doc = {"title": film, "business_model": model}
                coll.save(doc)
                if i>=29:
                    break
                if films_c >= 6213:
                    break
            print films_c
            pagenum+=1
        except:
            break
"""

def get_series():
    pagenum = 1
    series_c=0
    while pagenum <= 25:
        print pagenum
        try:
            page = urllib2.urlopen(menu["Сериалы"] + "/page" + str(pagenum))
            soup = BeautifulSoup(page.read())

            elems = soup.findAll("a", {"class": re.compile('^item-content-wrapper*')})
            for i, elem in enumerate(elems):
                series_c+=1
                tags = elem.findAll("span")
                model = tags[0].get("data-caption")
                series_name = tags[2].span.getText()
                doc = {"title": series_name, "business_model": model}
                coll.save(doc)
                if i >= 29:
                    break
                if series_c>=725:
                    break
            print series_c
            pagenum += 1
        except:
            break


'''Запросы в БД'''
"""

"""
def query():
    cursor.execute("select count(*), model from films group by model")
    for elem in cursor:
        print elem[0], elem[1]
"""
"""

#get_new()
#get_films()
get_series()
#query()


"""
