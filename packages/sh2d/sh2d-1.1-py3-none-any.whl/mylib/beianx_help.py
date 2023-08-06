#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import requests
from lxml import etree

requests.packages.urllib3.disable_warnings()

def beianx(name):
    '''
    :param name  支持公司名称、域名、备案号查询
    :return [{'目标': '', '主办单位': ' ', '单位性质': '', '网站备案号': '', '网站名称': '', '网站首页': '', '审核日期': '', '是否限制接入': ''}]
    '''
    result = []
    url = "https://www.beianx.cn/search/{}".format(name)
    headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"105\", \"Not)A;Brand\";v=\"8\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.54 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "close"}
    try:
        r = requests.get(url, headers=headers, verify=False)
        r.encoding = r.apparent_encoding
        html = etree.HTML(r.text)
        for tr in html.xpath('//tbody/tr'):
            info = {}
            info['主办单位'] = ''.join(tr.xpath('td[2]/a/text()')).strip()
            info['单位性质'] = ''.join(tr.xpath('td[3]/text()')).strip()
            info['网站备案号'] = ''.join(tr.xpath('td[4]/text()')).strip()
            info['网站名称'] = ''.join(tr.xpath('td[5]/text()')).strip()
            info['网站首页'] = ''.join(tr.xpath('td[6]/div/a/text()')).strip()
            info['审核日期'] = ''.join(tr.xpath('td[7]/div/text()')).strip()
            info['是否限制接入'] = ''.join(tr.xpath('td[8]/text()')).strip()
            result.append(info)
    except:
        pass

    return result

if __name__ == '__main__':
    name = '沪ICP备13033796号'
    print(beianx(name))