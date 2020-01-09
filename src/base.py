# -*- coding: utf-8 -*

import configparser
import random
import time
import requests
from lxml import etree

config = configparser.ConfigParser()
config.read('config.ini')
igneous = config['exhentai_cookie'].get('igneous')
ipb_member_id = config['exhentai_cookie'].get('ipb_member_id')
ipb_pass_hash = config['exhentai_cookie'].get('ipb_pass_hash')
sk = config['exhentai_cookie'].get('sk')
use_proxy = config['settings'].get('use_proxy')
cookies = {'ipb_member_id': ipb_member_id, 'ipb_pass_hash': ipb_pass_hash, 'igneous': igneous, "sk": sk}

session = requests.session()

if use_proxy == "True" or use_proxy == "true":
    http_proxy = config['settings'].get('http_proxy')
    https_proxy = config['settings'].get('https_proxy')
    session.proxies = {
        "http": http_proxy,
        "https": https_proxy
    }

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36 Edg/79.0.309.58',
    "Referer": 'https://exhentai.org/'
}


def get_fav():
    base_url = 'https://exhentai.org/favorites.php'
    base_response = session.get(base_url, headers=headers, cookies=cookies).text
    base_html_etree = etree.HTML(base_response)
    end_page_num = int(base_html_etree.xpath("/html/body/div[2]/form/table[1]/tr/td[last()-1]/a/text()")[0])
    print("Total", end_page_num, "pages.")
    end_page_num = input("Enter target end page num: ")
    url = 'https://exhentai.org/favorites.php?page='
    for count in range(int(end_page_num)):
        per_url = url + str(count)
        response = session.get(per_url, headers=headers, cookies=cookies).text
        html_etree = etree.HTML(response)
        titles = html_etree.xpath('/html/body/div[2]/form/table[2]/tr/td[3]/a/div[1]/text()')
        links = html_etree.xpath('/html/body/div[2]/form/table[2]/tr/td[3]/a/@href')
        for i in range(len(titles)):
            print(titles[i], links[i])
        time.sleep(random.uniform(0.5, 1.0))  # 暂停 0.5 ~ 1S，防止反爬


def get_top_list():
    url = "https://e-hentai.org/toplist.php"


if __name__ == '__main__':
    get_fav()
