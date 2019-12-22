# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy_douban.user_agents import agents
import random


class RotateUserAgentMiddleware(UserAgentMiddleware):
    def process_request(self, request, spider):
        user_agent = random.choice(agents)
        if user_agent:
            # print("********Current UserAgent:%s************" % user_agent)
            request.headers.setdefault(b'User-Agent', user_agent)
