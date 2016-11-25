#-*- coding:utf-8 -*-
import xml.etree.ElementTree as ET
tree = ET.parse('C:\\tv1000play.xml')
root = tree.getroot()


for event in root.findall("event"):
    film = {}
    for attr in event:

        if attr.tag != "licenses" and attr.tag != "video_file":
            film[attr.tag] = attr.text

        if attr.tag == "licenses":
            licenses = []
            for elem in attr:
                license = {}
                for field in elem:
                    license[field.tag] = field.text
                licenses.append(license)
            film[attr.tag] = licenses

        if attr.tag == "video_file":
            video = {}
            for elem in attr:
                video[elem.tag] = elem.text
            film[attr.tag] = video
    print(film)
