# from . import db
# from models import User, Store, Comment
import pymysql
import requests
from time import sleep
from aip import AipNlp
import random
import csv
import os
import datetime


def sentiment_ana(str):
    try:
        APP_ID = '15797847'
        API_KEY = 'Ciya2SWNN1i9ti3UZKXkaQxD'
        SECRET_KEY = 'hNjCqO6PBHCe7iGvId34v2Q5e5v9oYBN'
        client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
        result = client.sentimentClassify(str)
        score = result['items'][0]['positive_prob']
        score = score*10-5
    except ConnectionError as e:
        return None
    return score


def geocodeB(address):
    """
    @ address: 名称字符串
    @ 返回值：经度，纬度
    """
    if '合肥市' not in address:

        address = '合肥市'.join(address)
    try:
        base_url = "http://api.map.baidu.com/geocoder?address={address}&output=json&key=g3oOHh4TsL6Vp9hcNwUYfvriQsMBFiqd".format(address=address)
        response = requests.get(base_url)
        answer = response.json()
        status = answer['status']
        lng = answer['result']['location']['lng']
        lat = answer['result']['location']['lat']
    except ConnectionError as e:
        return status, None, None
    return status, lng, lat


def create_csv():
    basedir = os.path.dirname(__file__)

    connection = pymysql.connect(host='localhost', port=3306,
                                 user='root', password='000000', db='recommend')
    cur = connection.cursor()

    SQL = 'select * from storeinfo'
    cur.execute(SQL)
    result = cur.fetchall()
    header = ['storename', 'location', 'lng', 'lat', 'score', 'special', 'img_url']
    rows = []
    header_comment = ['comment', 'comment_score', 'comment_time']
    rows_comment = []
    for item in result:
        rows.append([item[1],
                     item[2],
                     'None',
                     'None',
                     item[7],
                     item[6],
                     item[5]])

        SQL = 'select * from storecomment where StoreNO = %s'
        cur.execute(SQL, (item[0]))
        inner = cur.fetchall()
        for tmp in inner:
            rows_comment.append([item[1], tmp[3], 'None', str(tmp[2]).split()[0]])


    with open(os.path.join(basedir, 'tmp', 'store.csv'), 'w', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    print('*' * 20, '商铺信息录入完成', '*' * 20)

    with open(os.path.join(basedir, 'tmp', 'comment.csv'), 'w', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(header_comment)
        writer.writerows(rows_comment)
    print('*' * 20, '评论信息录入完成', '*' * 20)


def add_id():
    basedir = os.path.dirname(__file__)

    connection = pymysql.connect(host='localhost', port=3306,
                                 user='root', password='000000', db='recommend')
    cur = connection.cursor()

    SQL = 'select * from storeinfo'
    cur.execute(SQL)
    result = cur.fetchall()
    header_comment = ['comment', 'comment_score', 'comment_time']
    rows_comment = []
    for item in result:
        SQL = 'select * from storecomment where StoreNO = %s'
        cur.execute(SQL, (item[0]))
        inner = cur.fetchall()
        for tmp in inner:
            rows_comment.append([item[1], tmp[3], 'None', str(tmp[2]).split()[0]])

    with open(os.path.join(basedir, 'tmp', 'comment.csv'), 'w', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(header_comment)
        writer.writerows(rows_comment)
    print('*' * 20, '评论信息录入完成', '*' * 20)



if __name__ == '__main__':
    create_csv()
