#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import json
import requests

requests.packages.urllib3.disable_warnings()

def aiqicha(name):
    result = []

    def page_parse_json(content):
        tag1 = "window.pageData ="
        tag2 = "window.isSpider ="
        idx1 = content.index(tag1)
        idx2 = content.index(tag2)
        try:
            new_content = content[idx1+len(tag1):idx2]
            new_content = new_content.replace("\n", "")
            new_content = new_content.replace(" ", "")
            new_content = new_content[:-1]
            cj = json.loads(new_content)
            for item in cj.get('result', {}).get('resultList', []):
                info = {}
                info['企业名称'] = item['titleName']
                info['法人代表'] = item['legalPerson']
                info['注册资本'] = item['regCap']
                info['成立时间'] = item['validityFrom']
                info['地址'] = item['domicile']
                info['统一信用社会代码'] = item['regNo']
                info['开业状态'] = item['openStatus']
                info['经营范围'] = item['scope']
                result.append(info)
        except:
            pass
    url = "https://aiqicha.baidu.com/s"
    params = {'q': name, 't': 0}
    headers = {"Referer": "https://aifanfan.baidu.com/", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43",
               "Accept": "text/html, application/xhtml+xml, image/jxr, */*", "Accept-Encoding": "gzip, deflate", "Connection": "close"}
    try:
        r = requests.get(url, params=params, headers=headers, verify=False)
        r.encoding = r.apparent_encoding
        page_parse_json(r.text)
    except:
        pass
    return result