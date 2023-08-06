#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import re
import ipaddress

from .common_help import num2numnum

def ip2num(ip):
    """
    IP转数字
    :param num: 1.1.1.3
    :return 232342343423432
    """
    return int(ipaddress.ip_address(ip))

def num2ip(num):
    """
    数字转IP
    :param num: 232342343423432
    :return 1.1.1.3
    """
    return ipaddress.ip_address(num).compressed

def gen_ip(start_ip,end_ip):
    """
    根据IP范围生成IP
    :param start_ip: 1.1.1.1
    :param end_ip: 1.1.1.3
    :return ['1.1.1.1','1.1.1.2']
    """
    return [num2ip(num) for num in range(ip2num(start_ip), ip2num(end_ip)+1)]

def net2ipip(net_str, strict=False):
    """
    转化单个其他网段格式成单个ip-ip格式
    :param net_str: 传入合法网段,eg: 192.168.1.0/24 or 192.168.1.1-33 or 192.168.1.5-192.168.1.8
    :return 返回 ['192.168.1.5','192.168.1.8']
    """
    if re.search(r"^\d+\.\d+\.\d+\.\d+-\d+$", net_str):
        _net, a, b = re.findall(r"(\d+\.\d+\.\d+\.)(\d+)-(\d+)", net_str)[0]
        ipip = [f'{_net}{a}',f'{_net}{b}']
    elif re.match(r"^\d+\.\d+\.\d+\.\d+-\d+\.\d+\.\d+\.\d+$", net_str):
        ipip = re.findall(r"(\d+\.\d+\.\d+\.\d+)-(\d+\.\d+\.\d+\.\d+)", net_str)[0]
    elif re.match(r'^[0-9a-fA-F]{1,4}:.*:[0-9a-fA-F]{1,4}-[0-9a-fA-F]{1,4}:.*:[0-9a-fA-F]{1,4}$', net_str):
        ipip = re.findall(r'([0-9a-fA-F]{1,4}:.*:[0-9a-fA-F]{1,4})-([0-9a-fA-F]{1,4}:.*:[0-9a-fA-F]{1,4})', net_str)[0]
    else:
        try:
            ipip = [ipaddress.ip_network(net_str, strict=strict).network_address.compressed,ipaddress.ip_network(net_str, strict=strict).broadcast_address.compressed]
        except Exception as e:
            ipip = ['0','0']
    return ipip


def net2ip(net_str, strict=False):
    """
    拆分单个网段为IP列表
    :param net_str: 传入合法网段,eg: 192.168.1.0/24 or 192.168.1.1-33 or 192.168.1.5-192.168.1.8
    :param strict: 是否校验网络地址 eg: False
    :return 返回list eg [ip1,ip2,...]
    """
    ipip = net2ipip(net_str, strict=strict)
    if ipip == ['0','0']:
        return []
    else:
        return gen_ip(*ipip)


def net2cidr(net_str, strict=False):
    """
    合并单个网段为cdir格式列表
    :param net_str: 传入合法网段,eg:  192.168.1.0/24 or 192.168.1.1-33 or 192.168.1.5-192.168.1.8
    :return 返回 ["192.168.1.0/24"]
    """
    ipip = net2ipip(net_str, strict=strict)
    try:
        return [ipaddr.compressed for ipaddr in ipaddress.summarize_address_range(
            ipaddress.IPv4Address(ipip[0]), ipaddress.IPv4Address(ipip[1]))]
    except:
        return []


def ip2ipip(iplist):
    """
    合并ip列表为ip-ip格式列表
    :param net_str: 传入合法网段,eg:  [ip1,ip2,...]
    :return 返回 ["ip1-ip2","ip3-ip4"]
    """
    num_iplist = [ip2num(_) for _ in iplist]
    numnumlist = num2numnum(num_iplist)
    return [[num2ip(a),num2ip(b)] for a, b in numnumlist]


def ip2cidr(iplist):
    """
    合并ip列表为cidr格式列表
    :param net_str: 传入合法网段,eg:  [ip1,ip2,...]
    :return 返回 ["ip1/24","ip3/32"]
    """

    num_iplist = [ip2num(_) for _ in iplist]
    numnumlist = num2numnum(num_iplist)
    cidr_list = []
    for a, b in numnumlist:
        try:
            cidr_list += [ipaddr.compressed for ipaddr in ipaddress.summarize_address_range(
                ipaddress.IPv4Address(num2ip(a)), ipaddress.IPv4Address(num2ip(b)))]
        except:
            pass
    return cidr_list


if __name__ == '__main__':
    pass
    print(net2ipip('2001:db8::1:0:0:1-2001:db8::1:0:0:3'))
