# 爬取 https://e-hentai.org/toplist.php 页面排行数据，返回 exhentai 链接
import configparser

import requests

config = configparser.ConfigParser()
config.read('config.ini')
igneous = config['exhentai_cookie'].get('igneous')
ipb_member_id = config['exhentai_cookie'].get('ipb_member_id')
ipb_pass_hash = config['exhentai_cookie'].get('ipb_pass_hash')
sk = config['exhentai_cookie'].get('sk')
cookies = {'igneous': igneous, 'ipb_member_id': ipb_pass_hash, 'ipb_pass_hash': ipb_pass_hash, "sk": sk}
url = "https://e-hentai.org/toplist.php"
session = requests.session()
use_proxy = config['settings'].get('use_proxy')
if use_proxy == "true":
    http_proxy = config['settings'].get('http_proxy')
    https_proxy = config['settings'].get('https_proxy')
    # print("Proxy: ", http_proxy, https_proxy)
    session.proxies = {
        "http": http_proxy,
        "https": https_proxy
    }

response = session.get(url)
print(str(response))
