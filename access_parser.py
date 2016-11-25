#-*- coding: utf-8 -*-
import xlrd
import pprint
from pymongo import MongoClient
import datetime

'''transforming data according to our needs'''
def int_transform(object):
    try:
        object = int(object)
    except:
        pass
    return object

def data_transform(object):
    try:
        year, month, day, hour, minute, second = xlrd.xldate_as_tuple(object, 0)
        object = datetime.datetime(year, month, day).strftime("%d.%m.%Y")
    except:
        pass
    return object

def float_transform(object):
    try:
        object = float(object)
    except:
        pass
    return object


'''connecting to mongodb'''
def connect_to_database():
    conn = MongoClient()
    conn = MongoClient('localhost', 27017)
    db = conn.access
    return db


'''move films from access to mongodb'''
def get_films_replace_database(db):
    db.films.drop()
    films_collection = db.films
    rb = xlrd.open_workbook("C:\\FILMS.xlsx")
    sheet = rb.sheet_by_index(0)
    for rownum in range(sheet.nrows-1):

        film = {}
        row = sheet.row_values(rownum+1)

        film["id"] = int_transform(row[0])
        film["type"] = row[1]
        film["rus_lat"] = row[2]
        film["rus_title"] = row[3]
        film["title"] = row[4]
        film["year"] = row[5]
        film["country"] = row[6]
        film["chron"] = row[7]
        film["age"] = row[8]
        film["id_kp"] = int_transform(row[9])
        film["id_imdb"] = row[10]
        film["dubbing"] = row[11]

        films_collection.save(film)


'''move licenses from access to mongodb'''
def get_licenses_replace_database(db):
    db.licenses.drop()
    licenses_collection = db.licenses
    rb = xlrd.open_workbook("C:\\LICENSES.xlsx")
    sheet = rb.sheet_by_index(0)
    for rownum in range(sheet.nrows - 1):

        license = {}
        row = sheet.row_values(rownum + 1)
        license["contract_id"] = int(row[0])
        license["film_id"] = int(row[1])
        license["distributor_id"] = int(row[2])
        license["license_start_date"] = data_transform(row[3])
        license["lcense_end_date"] = data_transform(row[4])
        license["shows_number"] = row[5]
        license["channels"] = row[6].split(",")
        license["add_date"] = data_transform(row[7])
        license["contragent_name"] = row[8]
        license["contragent_country"] = row[9]
        license["contragent_category"] = row[10]
        license["distributor_name"] = row[11]
        license["names_number"] = int_transform(row[12])
        license["conditions"] = row[13]

        licenses_collection.save(license)


'''move licenses from access to mongodb'''
def get_description_replace_database(db):
    db.descriptions.drop()
    descriptions_collection = db.descriptions
    rb = xlrd.open_workbook("C:\\DESCRIPTIONS.xlsx")
    sheet = rb.sheet_by_index(0)
    for rownum in range(sheet.nrows - 1):

        description = {}
        row = sheet.row_values(rownum + 1)
        description["film_id"] = row[0]
        description["studies"] = row[1]
        description["director"] = row[2]
        description["rus_director"] = row[3]
        description["composer"] = row[4]
        description["rus_composer"] = row[5]
        description["writers"] = row[6]
        description["rus_writers"] = row[7]
        description["cast"] = row[8].split(",")
        description["rus_cast"] = row[9].split(",")
        description["stars"] = row[10].split(",")
        description["rus_stars"] = row[11].split(",")
        description["source"] = row[12]
        description["more"] = row[13]
        description["key_words"] = row[14].split(",")
        description["group"] = row[15].split(",")
        description["rus_genre"] = row[16]
        description["genre"] = row[17]
        description["announcement"] = row[18]
        description["content"] = row[19]
        description["imdb_rate"] = float_transform(row[20])
        description["kp_rate"] = float_transform(row[21])
        description["budget"] = float_transform(row[22])
        description["rf_cash"] = float_transform(row[23])
        description["us_cash"] = float_transform(row[24])
        description["world"] = float_transform(row[25])

        descriptions_collection.save(description)



db = connect_to_database()
get_films_replace_database(db)
get_licenses_replace_database(db)
get_description_replace_database(db)
