# -*- coding: utf-8 -*-
import scrapy
import re

from scrapy import Request
from scrapy.http import request

from ..items import ScrapyDoubanItem


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com', 'movie.douban.com']
    url = "https://movie.douban.com/top250"
    start_urls = [url]

    # def start_requests(self):
    #     """
    #     在此添加header中的User-Agent，如果没有会报403错误
    #     注释原因：开始报403错误时，在此设置UA，随后在中间件处设置了随机UA，故此处应该注释
    #     :return:
    #     """
    #     ua = random.choice(agents)
    #     print("-----------------------", ua)
    #     yield Request(url=self.url, headers={"User-Agent": ua})
    #     print("执行到这里")
    #     yield Request(url=self.url)

    def __init__(self, name=None, **kwargs):
        super().__init__(name=None, **kwargs)
        self.parse_detail = None

    def parse(self, response):
        item = ScrapyDoubanItem()
        title_ch = response.xpath('//div[@class="hd"]/a/span[1]/text()').extract()
        item["title_ch"] = [i.strip() for i in title_ch]
        x_ = response.xpath('//div[@class="bd"]/p[1]')

        item['detail'] = [i.strip().replace('\xa0', ' ').replace('...', '').replace('/', '') for i in x_.xpath('./text()[1]').extract()]

        content = x_.xpath('./text()[2]').extract()
        item["release_time"] = [i.split("/")[0].strip() for i in content]
        item["release_location"] = [i.split("/")[1].strip() for i in content]
        item["category"] = [i.split("/")[2].strip() for i in content]
        item["rating_num"] = response.xpath('//div[@class="star"]/span[@class="rating_num"]/text()').extract()
        item["rating_count"] = [re.search(r'(\d+)', i)[0] for i in response.xpath('//div[@class="star"]/span[4]/text()').extract()]
        item["quote"] = response.xpath('//div[@class="bd"]/p[@class="quote"]/span/text()').extract()
        item["image_url"] = [i[:-4] for i in response.xpath('//div[@class="pic"]/a/img/@src').extract()]
        item["top_id"] = response.xpath('//div[@class="pic"]/em/text()').extract()

        # 详情页信息
        detail_url = response.xpath('//div[@class="pic"]/a/@href').extract()
        for url in detail_url:
            yield Request(url=url, callback=self.parse_detail, meta={'item': item}, dont_filter=True)

        # 下一页
        # next_url = response.xpath('//link[@rel="next"]/@href').extract_first()
        # if next_url:
        #     next_url = self.url + next_url
        #     yield scrapy.Request(next_url, callback=self.parse)

    def parse_detail(self, response):
        """
        二级页面爬取
        :param response:
        :param item:
        :return:
        """
        item = response.meta['item']
        item['director'] = response.xpath('//div[@id="info"]/span[1]/span[2]/a/text()').extract_first()
        item['screenwriter'] = response.xpath('//div[@id="info"]/span[2]/span[2]/a/text()').extract()
        item['starring'] = response.xpath('//div[@id="info"]/span[@class="actor"]/span[2]//a/text()').extract()
        item['length'] = response.xpath('//div[@id="info"]/span[@property="v:runtime"]/text()').extract()
        introduction = response.xpath('//div[@id="link-report"]/span[@class="all hidden"]/text()').extract()
        for i in introduction:
            i = i.strip()
            item['introduction'] += i
        item['hot_comment_by'] = response.xpath('//div[@data-cid]//header/a[2]/text()').extract()
        item['comment_by_url'] = response.xpath('//div[@data-cid]//header/a[2]/@href').extract()
        item['comment_by_image'] = response.xpath('//div[@data-cid]//header/a[1]/img/@src').extract()
        item['comment_time'] = response.xpath('//div[@data-cid]//header/span[2]/text()').extract()
        item['comment'] = [i.strip().replace('\xa0(', '').strip() for i in
                           response.xpath('//div[@data-cid]//div[@class="main-bd"]//div[@class="short-content"]/text()[1').extract()]
        item['like'] = [i.strip() for i in response.xpath('//div[@data-cid]//div[@class="action"]/a[1]/span/text()').extract()]
        item['dislike'] = [i.strip() for i in response.xpath('//div[@data-cid]//div[@class="action"]/a[2]/span/text()').extract()]

        print("解析完毕")
        print("执行到这")
        print(item)
        print("跳过item了")
        yield item



