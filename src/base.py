# -*- coding: utf-8 -*

import configparser
import datetime
import logging
import os
import random
import sys
import time
import pymysql
import requests
from lxml import etree


def get_fav():
    base_url = 'https://exhentai.org/favorites.php'
    base_response = session.get(
        base_url, headers=headers, cookies=cookies).text
    base_html_etree = etree.HTML(base_response)
    end_page_num = int(base_html_etree.xpath(
        "/html/body/div[2]/form/table[1]/tr/td[last()-1]/a/text()")[0])
    print("Total", end_page_num, "pages.")
    end_page_num = input("Enter target end page num: ")
    url = 'https://exhentai.org/favorites.php?page='
    for count in range(int(end_page_num)):
        per_url = url + str(count)
        response = session.get(per_url, headers=headers, cookies=cookies).text
        html_etree = etree.HTML(response)
        titles = html_etree.xpath(
            '/html/body/div[2]/form/table[2]/tr/td[3]/a/div[1]/text()')
        links = html_etree.xpath(
            '/html/body/div[2]/form/table[2]/tr/td[3]/a/@href')
        for i in range(len(titles)):
            title = titles[i]
            link = links[i]
            cursor = db_cnct.cursor()
            cursor.execute(
                "INSERT INTO favorites VALUES( null, %s, %s, null)", (title, link))
            db_cnct.commit()
        time.sleep(random.uniform(0.3, 0.5))
    time.sleep(random.uniform(0.5, 1.0))


def e2ex(e_link):
    return str(e_link).replace('e-hentai', 'exhentai')


def get_top_list():
    url = "https://e-hentai.org/toplist.php"
    resp = session.get(url, headers={"User-Agent": user_agent}).text
    html_etree = etree.HTML(resp)
    past_year_titles = html_etree.xpath(
        '/html/body/div[2]/div[1]/div[2]/table/tr/td[2]/div/a/text()')
    past_year_links = html_etree.xpath(
        '/html/body/div[2]/div[1]/div[2]/table/tr/td[2]/div/a/@href')
    for i in range(len(past_year_titles)):
        cursor = db_cnct.cursor()
        cursor.execute("INSERT INTO toplist VALUES( null, %s, %s, null, %s, %s)", (
            past_year_titles[i], e2ex(
                past_year_links[i]), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'yearly'))
        db_cnct.commit()
    past_month_titles = html_etree.xpath(
        '/html/body/div[2]/div[1]/div[3]/table/tr/td[2]/div/a/text()')
    past_month_links = html_etree.xpath(
        '/html/body/div[2]/div[1]/div[3]/table/tr/td[2]/div/a/@href')
    for i in range(len(past_month_titles)):
        cursor = db_cnct.cursor()
        cursor.execute("INSERT INTO toplist VALUES( null, %s, %s, null, %s, %s)", (
            past_month_titles[i], e2ex(
                past_month_links[i]), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'monthly'))
        db_cnct.commit()
    yesterday_titles = html_etree.xpath(
        '/html/body/div[2]/div[1]/div[4]/table/tr/td[2]/div/a/text()')
    yesterday_links = html_etree.xpath(
        '/html/body/div[2]/div[1]/div[4]/table/tr/td[2]/div/a/@href')
    for i in range(len(yesterday_titles)):
        cursor = db_cnct.cursor()
        cursor.execute("INSERT INTO toplist VALUES( null, %s, %s, null, %s, %s)", (
            yesterday_titles[i], e2ex(
                yesterday_links[i]), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'yesterday'))
        db_cnct.commit()
    time.sleep(random.uniform(0.1, 0.3))


def db_connect(host, port, username, password, db):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            passwd=password,
            db=db
        )
        connection.set_charset("utf8mb4")
        return connection
    except Exception as e:
        logging.error('Failed to connect to MySQL. {}'.format(str(e)))
        sys.exit(-1)


def get_col_index(spec_col_name, filed_names):
    return filed_names.index(spec_col_name)


def get_field_names(cnct, sql):
    cursor = cnct.cursor()
    cursor.execute(sql)
    field_names = [d[0] for d in cursor.description]
    cursor.close()
    return field_names


def execute_sql(cursor, sql, num, connection):
    try:
        cursor.execute(sql)
        if num == 0:
            result = cursor.fetchall()
        else:
            result = cursor.fetchmany(num)
        return result
    except Exception as e:
        logging.error("Failed to execute sql: %s\nSQL: %s" % (str(e), sql))
        connection.rollback()
    finally:
        cursor.close()


def set_proxy():
    if use_proxy == "True" or use_proxy == "true":
        http_proxy = config['settings'].get('http_proxy')
        https_proxy = config['settings'].get('https_proxy')
        session.proxies = {
            "http": http_proxy,
            "https": https_proxy
        }


# TODO: use official API
if __name__ == '__main__':
    base_path = os.path.dirname(os.path.realpath(__file__))
    log_file_full_path = os.path.join(base_path, "exhentai_py.log")
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.INFO,
                        filename=log_file_full_path, filemode='a')

    config = configparser.ConfigParser()
    config.read('config.ini')
    igneous = config['exhentai_cookie'].get('igneous')
    ipb_member_id = config['exhentai_cookie'].get('ipb_member_id')
    ipb_pass_hash = config['exhentai_cookie'].get('ipb_pass_hash')
    sk = config['exhentai_cookie'].get('sk')
    use_proxy = config['settings'].get('use_proxy')
    mysql_host = config['MySQL'].get('host')
    mysql_port = config['MySQL'].get('port')
    mysql_user = config['MySQL'].get('user')
    mysql_password = config['MySQL'].get('password')
    mysql_dbname = config['MySQL'].get('dbname')

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36 Edg/79.0.309.58'
    headers = {"User-Agent": user_agent, "Referer": 'https://exhentai.org/'}
    cookies = {'ipb_member_id': ipb_member_id, 'ipb_pass_hash': ipb_pass_hash, 'igneous': igneous, "sk": sk}
    session = requests.session()
    set_proxy()

    db_cnct = db_connect(mysql_host, mysql_port, mysql_user, mysql_password, mysql_dbname)

    get_top_list()
    # get_fav()  # 仅用作 telegram bot 的话记得注释掉
    db_cnct.close()
