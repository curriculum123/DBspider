# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyDoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title_ch = scrapy.Field()  # 中文名
    detail = scrapy.Field()  # 导演主演等信息
    release_time = scrapy.Field()  # 上映时间
    release_location = scrapy.Field()  # 上映地点
    category = scrapy.Field()  # 类别
    rating_num = scrapy.Field()  # 分值
    rating_count = scrapy.Field()  # 评论人数
    quote = scrapy.Field()  # 短评
    image_url = scrapy.Field()  # 封面图片地址
    top_id = scrapy.Field()  # 排名

    # 详情页
    director = scrapy.Field()  # 导演
    screenwriter = scrapy.Field()  # 编剧
    starring = scrapy.Field()  # 主演
    # language = scrapy.Field()  # 语言
    length = scrapy.Field()  # 时长
    introduction = scrapy.Field()  # 简介
    hot_comment_by = scrapy.Field()  # 评论者
    comment_by_url = scrapy.Field()  # 评论者的地址
    comment_by_image = scrapy.Field()  # 评论者的头像
    comment_time = scrapy.Field()  # 评论时间
    comment = scrapy.Field()  # 评论
    like = scrapy.Field()  # 赞
    dislike = scrapy.Field()  # 踩







