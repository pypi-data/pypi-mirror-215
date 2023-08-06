#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import time
import cv2
import base64
import hashlib
import requests

requests.packages.urllib3.disable_warnings()

def beian(name):
    '''
    :param name  支持公司标准名称、域名、备案号查询
    :return [{'目标': '', '主办单位': ' ', '单位性质': '', '网站备案号': '', '审核日期': '', '是否限制接入': ''}]
    '''
    result = []
    headers = {
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Microsoft Edge";v="90"',
        'Accept': 'application/json, text/plain, */*',
        'DNT': '1',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.46',
        'Origin': 'https://beian.miit.gov.cn',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://beian.miit.gov.cn/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'}
    try:
        # 获取 __jsluid_s
        __jsluid_s = requests.utils.dict_from_cookiejar(requests.get(
            'https://beian.miit.gov.cn/', headers=headers).cookies)['__jsluid_s']
        # 获取token
        timeStamp = int(round(time.time()*1000))
        authSecret = 'testtest' + str(timeStamp)
        authKey = hashlib.md5(authSecret.encode(encoding='UTF-8')).hexdigest()
        rj1 = requests.post('https://hlwicpfwc.miit.gov.cn/icpproject_query/api/auth', data={
                            'authKey': authKey, 'timeStamp': timeStamp}, headers={**headers, **{'Cookie': '__jsluid_s='+__jsluid_s}}).json()
        if rj1['success']:
            token = rj1['params']['bussiness']
            # 获取验证图像、UUID
            rj2 = requests.post('https://hlwicpfwc.miit.gov.cn/icpproject_query/api/image/getCheckImage',
                                data='', headers={**headers, **{'Cookie': '__jsluid_s='+__jsluid_s, 'token': token}}).json()
            if rj2['success']:
                p_uuid = rj2['params']['uuid']
                big_image = rj2['params']['bigImage']
                small_image = rj2['params']['smallImage']
                # 解码图片，写入并计算图片缺口位置
                with open('bigImage.jpg', 'wb') as f:
                    f.write(base64.b64decode(big_image))
                    f.close()
                with open('smallImage.jpg', 'wb') as f:
                    f.write(base64.b64decode(small_image))
                    f.close()
                background_image = cv2.imread(
                    'bigImage.jpg', cv2.COLOR_GRAY2RGB)
                fill_image = cv2.imread('smallImage.jpg', cv2.COLOR_GRAY2RGB)
                position_match = cv2.matchTemplate(
                    background_image, fill_image, cv2.TM_CCOEFF_NORMED)
                _, _, _, max_loc = cv2.minMaxLoc(position_match)
                mouse_length = max_loc[0]+1
                # 通过拼图验证，获取sign
                rj3 = requests.post('https://hlwicpfwc.miit.gov.cn/icpproject_query/api/image/checkImage', json={'key': p_uuid, 'value': mouse_length}, headers={
                                    **headers, **{'Cookie': '__jsluid_s='+__jsluid_s, 'token': token, 'Content-Type': 'application/json'}}).json()
                if rj3['success']:
                    sign = rj3['params']
                    # 获取备案信息
                    rj4 = requests.post('https://hlwicpfwc.miit.gov.cn/icpproject_query/api/icpAbbreviateInfo/queryByCondition', json={'pageNum': '', 'pageSize': '', 'unitName': name}, headers={
                                        **headers, **{'Cookie': '__jsluid_s='+__jsluid_s, 'token': token, 'sign': sign, 'uuid': p_uuid, 'Content-Type': 'application/json'}}).json()
                    if rj4['success']:
                        for item in rj4['params']['list']:
                            info = {}
                            info['域名'] = item['domain']
                            info['主办单位'] = item['unitName']
                            info['单位性质'] = item['natureName']
                            info['网站备案号'] = item['serviceLicence']
                            info['审核日期'] = item['updateRecordTime']
                            info['是否限制接入'] = item['limitAccess']
                            result.append(info)
                        total_page = rj4['params']['pages']
                        if total_page > 1:
                            for i in range(1, total_page):
                                rj5 = requests.post('https://hlwicpfwc.miit.gov.cn/icpproject_query/api/icpAbbreviateInfo/queryByCondition', json={'pageNum': i+1, 'pageSize': 10, 'unitName': name}, headers={
                                                    **headers, **{'Cookie': '__jsluid_s='+__jsluid_s, 'token': token, 'sign': sign, 'uuid': p_uuid, 'Content-Type': 'application/json'}}).json()
                                if rj5['success']:
                                    for item in rj5['params']['list']:
                                        info = {}
                                        info['域名'] = item['domain']
                                        info['主办单位'] = item['unitName']
                                        info['单位性质'] = item['natureName']
                                        info['网站备案号'] = item['serviceLicence']
                                        info['审核日期'] = item['updateRecordTime']
                                        info['是否限制接入'] = item['limitAccess']
                                        result.append(info)
                                else:
                                    print('获取备案信息', i+1, rj5['msg'])
                    else:
                        print('获取备案信息', rj4['msg'])
                else:
                    print('通过拼图验证，获取sign', rj3['msg'])
            else:
                print('获取验证图像、UUID', rj2['msg'])
        else:
            print('获取token', rj1['msg'])
    except:
        pass

    try:
        os.remove('bigImage.jpg')
        os.remove('smallImage.jpg')
    except:
        pass
    return result

if __name__ == '__main__':
    name = '沪ICP备13033796号'
    print(beian(name))