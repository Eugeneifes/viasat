# -*- coding: utf-8 -*-


import xlrd
import datetime
import pprint
path = ("C:\\TM#300152 - MGM Bond package - TV1000 P,M Test.xlsx")


rb = xlrd.open_workbook(path)
sheet = rb.sheet_by_index(1)
print sheet.name


database = {}

def to_date(date):
    year, month, day, hour, minute, second = xlrd.xldate_as_tuple(date, rb.datemode)
    return datetime.date(year, month, day).strftime("%Y-%m-%d")



def get_contract_info(database):

    contract = {}
    for rownum in range(1, 11):
        row = sheet.row_values(rownum)
        if row[1].strip()[:-1] == "Contract number":
            contract[row[1].strip()[:-1]] = int(row[2])
        else:
            contract[row[1].strip()[:-1]] = row[2]
    pprint.pprint(contract)
    print "\n"
    database["contract"] = contract
    return database

def get_films(database):
    film = {}
    for rownum in range(14, sheet.nrows):
        row = sheet.row_values(rownum)
        film["Product Code"] = str(int(row[1]))
        film["Title"] = row[2]
        film["Production Year"] = str(int(row[4]))
        film["Production Country"] = row[5]
        film["Production Language"] = row[6]
        film["VOD rights"] = row[7]
        film["Region Group"] = row[8]
        film["VOD Channels"] = row[9]
        film["Advertising"] = row[10]
        film["Exclusivity"] = row[11]
        film["Start Date"] = to_date(row[12])
        film["End Date"] = to_date(row[13])
        film["Earlieast allowed LPSD"] = row[14]
        film["Latest allowed LPSD"] = row[15]
        film["Consumption"] = row[16]
        film["Subs/Dubs"] = row[17]
        film["Other Comments"] = row[18]

        database[row[2]] = film
        film = {}
    return database


database = get_contract_info(database)
database = get_films(database)
pprint.pprint(database)
