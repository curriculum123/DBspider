# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os

from pymongo import MongoClient
import pymysql
from scrapy.exceptions import DropItem

from scrapy_douban import settings
import os
import requests
import random
from .user_agents import agents
from threading import Thread


class DownloadImageFilePipeline(object):
    """
    功能：下载图片-电影封面图
    set_header：创建header头的UA， 这个可用可不用，不设置的时候也是返回200，设置上只为了保险起见
    download_image：下载图片
    _createImageName：创建图片名称，这里采用的是 top_id 和 title_ch 相结合命名
    process_item：使用了多线程，提高下载速度
    """
    def set_header(self):
        headers = {
            'User-Agent': random.choice(agents)
        }
        return headers

    def download_image(self,file_path, url):
        try:
            with open(file_path, 'wb') as f:
                print("正在下载：" + url)
                content = requests.get(url, headers=self.set_header()).content
                f.write(content)
        except Exception as e:
            return None

    def _createImageName(self, item):
        length = len(item['top_id'])
        return [item['top_id'][i] + '-' + item['title_ch'][i] + '.jpg' for i in range(length)]

    def process_item(self, item, spider):
        name_list = self._createImageName(item)
        dir_path = '%s\%s' % (settings.IMAGES_STORE, spider.name)
        print(dir_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        for i in range(len(name_list)):
            image_url = item['image_url'][i]
            file_name = name_list[i]
            file_path = '%s\%s' % (dir_path, file_name)
            if os.path.exists(file_path):
                print("重复： " + image_url)
                continue
            t = Thread(target=self.download_image, args=(file_path, image_url))
            t.start()
        t.join()
        return item


class DoubanToMysqlPipeline(object):
    """
    如果更改其他mysql数据库,只需要更改settings中的属性即可
    :param
    :return
    """
    def __init__(self):
        self.client = pymysql.connect(
            host=settings.MYSQL_HOST or '127.0.0.1',
            port=settings.MYSQL_PORT or 3306,
            user=settings.MYSQL_USER or 'root',
            passwd=settings.MYSQL_PASSWD or 'root',
            db=settings.MYSQL_DBNAME or 'sc_dou',
            charset=settings.MYSQL_CHARSET or 'utf8'
        )
        self.cur = self.client.cursor()

    # pipeline默认调用
    def process_item(self, item, spider):
        sql = "insert into books(top_id,image_url,title_ch,detail,category,rating_count,release_location" \
              ",rating_num,quote,release_time)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        for i in range(len(item['top_id'])):
            params = (item["top_id"][i], item["image_url"][i], item["title_ch"][i], item["detail"][i],
                      item["category"][i], item["rating_count"][i], item["release_location"][i], item["rating_num"][i],
                      item["quote"][i], item["release_time"][i])
            self.cur.execute(sql, params)
        self.client.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.client.close()


class JsonWriterPipeline(object):
    """
    官网上的，保存为json格式
    如果不需要，可以在settings中的ITEM_PIPELINES关闭
    """
    def open_spider(self, spider):
        self.file = open('items.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item


class DoubanToMongoPipeline(object):
    """
    保存至mongodb
    """
    def __init__(self):
        self.mongo_uri = 'mongodb://127.0.0.1:27017/'
        self.db_name = 'sc_dou'  # 数据库名
        self.t_name = 'dou'  # 集合名
        self.client = MongoClient(self.mongo_uri)  # 创建数据库连接
        self.db = self.client[self.db_name]
        self.table = self.db[self.t_name]  # 创建集合的游标

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.table.insert(dict(item))
        return item
