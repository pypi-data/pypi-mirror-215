#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import requests
from lxml import etree

requests.packages.urllib3.disable_warnings()

def whois(domain):
    '''
    :param domain  域名
    :return [{'域名': '', '注册商': ' ', '联系人': '', '联系邮箱': '', '创建时间': '', '过期时间': ''}]
    '''
    result = []
    info = {}
    info['域名'] = domain
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}
    try:
        r = requests.get(
            f'https://whois.chinaz.com/{domain}', headers=headers, verify=False)
        r.encoding = r.apparent_encoding
        html = etree.HTML(r.text)
        whois_info = html.xpath('//*[@id="whois_info"]')[0]
        info['注册商'] = ''.join(whois_info.xpath(
            '//div[text()="注册商"]/following-sibling::*[1]/div/span/text()'))
        info['联系人'] = ''.join(whois_info.xpath(
            '//div[text()="联系人"]/following-sibling::*[1]/span/text()'))
        info['联系邮箱'] = ''.join(whois_info.xpath(
            '//div[text()="联系邮箱"]/following-sibling::*[1]/span/text()'))
        info['创建时间'] = ''.join(whois_info.xpath(
            '//div[text()="创建时间"]/following-sibling::*[1]/span/text()'))
        info['过期时间'] = ''.join(whois_info.xpath(
            '//div[text()="过期时间"]/following-sibling::*[1]/span/text()'))
    except:
        pass
    result.append(info)
    return result

def ipbatch(ips):
    '''
    :param ips  IP列表,单次限300
    :return [{'域名/IP': '', '获取的IP地址': '', '数字地址': '', 'IP的物理位置': ''},]
    '''
    result = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}
    try:
        data = {'ips': '\r\n'.join(ips), 'submore': '查询'}
        r = requests.post("https://ip.tool.chinaz.com/ipbatch",
                          data=data, headers=headers, verify=False)
        r.encoding = r.apparent_encoding
        html = etree.HTML(r.text)
        ipList = html.xpath('//*[@id="ipList"]')[0]
        for tr in ipList.xpath('tr'):
            info = {}
            info['域名/IP'] = ''.join(tr.xpath('td[1]/text()')).strip()
            info['获取的IP地址'] = ''.join(tr.xpath('td[2]/a/text()')).strip()
            info['数字地址'] = ''.join(tr.xpath('td[3]/text()')).strip()
            info['IP的物理位置'] = ''.join(tr.xpath('td[4]/text()')).strip()
            result.append(info)
    except:
        pass

    return result

def icp(domains):
    '''
    :param domains  域名列表,单次限20
    :return [{'域名': '', '主办单位': '', '单位性质': '', '备案号': '', '网站名称': '', '网站首页': '', '审核时间': '', '最近检测': ''},]
    '''
    result = []
    try:
        url = "https://micp.chinaz.com/Icp/BatchSearchs/"
        headers = {"Cache-Control": "max-age=0", "Sec-Ch-Ua": "\"Chromium\";v=\"105\", \"Not)A;Brand\";v=\"8\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Upgrade-Insecure-Requests": "1", "Origin": "https://micp.chinaz.com", "Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.54 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://micp.chinaz.com/Icp/BatchSearchs/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9"}
        data = {"hosts": '\r\n'.join(domains)}
        r = requests.post(url,
                          data=data, headers=headers, verify=False)
        r.encoding = r.apparent_encoding
        html = etree.HTML(r.text)
        for table in html.xpath('//table'):
            info = {}
            info['域名'] = ''.join(table.xpath('thead/tr/td/a/text()')).strip()
            info['主办单位'] = ''.join(table.xpath('tbody/tr[1]/td[2]/text()')).strip()
            info['单位性质'] = ''.join(table.xpath('tbody/tr[2]/td[2]/text()')).strip()
            info['备案号'] = ''.join(table.xpath('tbody/tr[3]/td[2]/text()')).strip()
            info['网站名称'] = ''.join(table.xpath('tbody/tr[4]/td[2]/text()')).strip()
            info['网站首页'] = ''.join(table.xpath('tbody/tr[5]/td[2]/text()')).strip()
            info['审核时间'] = ''.join(table.xpath('tbody/tr[6]/td[2]/text()')).strip()
            info['最近检测'] = ''.join(table.xpath('tbody/tr[7]/td[2]/text()')).strip()
            result.append(info)
    except:
        pass

    return result



if __name__ == '__main__':
    domain = 'freebuf.com'
    print(whois(domain))
    ips = ['8.8.8.8','114.114.114.114']
    print(ipbatch(ips))
    domains = ['baidu.com','freebuf.com']
    print(icp(domains))