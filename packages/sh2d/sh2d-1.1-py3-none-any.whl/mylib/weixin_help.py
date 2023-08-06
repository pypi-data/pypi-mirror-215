#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import time
import random
import requests


class Weixin:

    def __init__(self, token, cookie):
        self.token = token
        self.headers = {
            "cookie": cookie,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        }

    def get_fakid(self, name):
        url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz'
        data = {
            'action': 'search_biz',
            'scene': 1,
            'begin': 0,
            'count': 10,
            'query': name,
            'token': self.token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
        }
        # 发送请求
        rj = requests.get(url, headers=self.headers, params=data).json()
        # 获取公众号名称、fakeid
        wpub = {item['nickname']: item['fakeid'] for item in rj['list']}
        return wpub.get(name)

    def get_urls(self, fakeid, start_page=1, page_num=0):
        url = 'https://mp.weixin.qq.com/cgi-bin/appmsg'
        data = {
            'action': 'list_ex',
            'begin': start_page + page_num * 5, 
            'count': '5',
            'fakeid': fakeid,
            'type': '9',
            'query': '',
            'token': self.token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
        }
        time.sleep(random.randint(1, 3))
        rj = requests.get(url, headers=self.headers, params=data).json()
        return [{'name':name,'update_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i['update_time'])), 'title':i['title'], 'link':i['link']} for i in rj['app_msg_list']]

if __name__ == '__main__':
    token = ''
    cookie = ''
    name = ''
    fakeid = ''
    wx = Weixin(token, cookie)
    # fakeid = wx.get_fakid(name)
    print(fakeid)
    res = wx.get_urls(fakeid)
    print(res)
