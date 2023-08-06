#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import re
import requests

requests.packages.urllib3.disable_warnings()

def webinfo(url):
    result = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}
    info = {}
    info['目标'] = url
    url = url if '://' in url else 'http://' + url
    info['URL'] = url
    try:
        r = requests.get(url, headers=headers, verify=False)
        r.encoding = r.apparent_encoding
        info['状态码'] = str(r.status_code)
        info['网站标题'] = ''.join(re.findall('<title>(.*?)</title>', r.text))
        info['ICP备案号'] = ''.join(re.findall(
            '([\u4e00-\u9fa5]ICP[备证]\d+?号(?:-\d{1,3})?)', r.text))
    except:
        pass
    result.append(info)
    return result