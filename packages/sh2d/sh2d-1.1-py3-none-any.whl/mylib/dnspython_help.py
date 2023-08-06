#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import dns.resolver


def domain2ip(domain, dns_server=None):
    """
    解析域名到IP
    :param domian: 域名
    :param dns_server: DNS服务器
    :return [] ip列表
    """
    resolver = dns.resolver.Resolver()

    if dns_server is not None:
        resolver.nameservers = [dns_server]
    try:
        answer = resolver.resolve(domain, 'A')
        return [str(ip) for ip in answer]
    except:
        return []


def domain2cname(domain,dns_server=None):
    """
    查询CNAME
    :param domian: 域名
    :param dns_server: DNS服务器
    :return [] CNAME列表
    """
    resolver = dns.resolver.Resolver()

    if dns_server is not None:
        resolver.nameservers = [dns_server]
    try:
        answer = resolver.query(domain, 'CNAME')
        return [str(_.target).strip(".").lower() for _ in answer]
    except:
        return []

if __name__ == '__main__':
    domain = 'www.baidu.com'
    print(domain,domain2ip(domain),domain2cname(domain))
