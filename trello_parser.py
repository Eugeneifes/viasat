#-*- coding: utf-8 -*-
import json
import xlwt
import urllib2
from Tkinter import *
import os

def parse():

    board = e1.get()
    """получаем список листов"""
    lists_query = "https://api.trello.com/1/boards/" +board+ "/lists?key=" +key+ "&token="+token
    request = urllib2.urlopen(lists_query)
    lists = json.loads(request.read())

    """получаем список карточек"""
    cards_query = "https://api.trello.com/1/boards/" +board+ "/cards?key=" +key+ "&token="+token
    request = urllib2.urlopen(cards_query)
    cards = json.loads(request.read())

    """получаем список членов"""
    members_query = "https://api.trello.com/1/boards/" +board+ "/members?key=" +key+ "&token="+token
    request = urllib2.urlopen(members_query)
    members = json.loads(request.read())


    i=0
    j=0
    cards_count = 0
    for list in lists:
        for card in cards:
            if card["idList"] == list["id"]:
                cards_count+=1
                ws.write(j, 1, card["name"])
                try:
                    ws.write(j, 2, card["due"][:10])
                except:
                    pass
                name_list=""
                for id in card["idMembers"]:
                    for elem in members:
                        if id == elem["id"]:
                            name_list+=elem["username"]+" "
                ws.write(j, 3, name_list)
                j+=1
        ws.write_merge(i, i + cards_count - 1, 0, 0, list["name"])
        i+=cards_count
        cards_count = 0
    wb.save(save)


save = os.getcwd() + "/output.xls"

wb = xlwt.Workbook()
ws = wb.add_sheet('Sheet1')


with open("params.txt", "r") as file:
    lines = file.readlines()
    token = lines[0]
    key = lines[1]


master = Tk()
Label(master, text="Board_id").grid(row=0)
e1 = Entry(master)
e1.grid(row=0, column=1)
Button(master, text='Parse', command=parse).grid(row=3, column=1, sticky=W, pady=4)
mainloop()
