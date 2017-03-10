import requests
from bs4 import BeautifulSoup
import json

"display fpltable"

'''https://www.sslproxies.org/'''
def get_proxies_sslproxies_org(last_proxy):

    soup = BeautifulSoup(requests.get('https://www.sslproxies.org/').text)
    table = soup.find_all("table", class_="display fpltable")
    trs = table[0].find_all("tr")
    addresses = trs[1:len(trs)-1]
    for address in addresses:
        ip = address.td.text
        port = address.find_next("td").find_next("td").text
        if {"http": ip+":"+port} != last_proxy:
            return {"http": ip+":"+port}
        else:
            pass


def check_proxy_id(proxy):
    my_ip_info = json.loads(requests.get("http://httpbin.org/ip").text)
    my_ip = my_ip_info["origin"]
    proxy_ip_info = json.loads(requests.get("http://httpbin.org/ip", proxies=proxy).text)
    proxy_ip = proxy_ip_info["origin"]
    print(proxy_ip, my_ip)

def check_proxy_headers(proxy):
    my_headers_info = json.loads(requests.get("http://httpbin.org/headers").text)
    print(my_headers_info)
    my_headers = my_headers_info["headers"]
    proxy_headres_info = json.loads(requests.get("http://httpbin.org/headers", proxies=proxy).text)
    print(proxy_headres_info)
    proxy_headers = proxy_headres_info["headers"]
    print(my_headers, proxy_headers)

last_proxy = {"http": "36.81.185.7:80"}

"""
while(True):
    check_proxy_ip(last_proxy)
    last_proxy = get_proxies_sslproxies_org(last_proxy)
"""

#get_proxies_sslproxies_org()

check_proxy_headers({"http": "203.140.78.67:8080"})