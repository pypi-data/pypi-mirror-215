#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from itertools import groupby


def mask2num(mask):
    """
    掩码转数字
    :param mask: 255.255.255.255
    :return 32
    """
    def count_bit(bin_str): return len([i for i in bin_str if i == '1'])
    mask_splited = mask.split('.')
    mask_count = [count_bit(bin(int(i))) for i in mask_splited]
    return sum(mask_count)


def num2mask(mask_int):
    """
    数字转掩码
    :param mask_int: 32
    :return 255.255.255.255
    """
    bin_arr = ['0' for i in range(32)]
    for i in range(mask_int):
        bin_arr[i] = '1'
    tmpmask = [''.join(bin_arr[i * 8:i * 8 + 8]) for i in range(4)]
    tmpmask = [str(int(tmpstr, 2)) for tmpstr in tmpmask]
    return '.'.join(tmpmask)


def num2numnum(numlist):
    """
    根据数字列表生成数字范围列表
    :param numlist: [1,2,18,3,5,6,7,8,13,12,11,10]
    :return [[1,3],[5,8],[10,13]]
    """
    numlist.sort()
    numnumlist = []
    def fun(x): return x[1] - x[0]
    for k, g in groupby(enumerate(numlist), fun):
        _ = [v for i, v in g]
        if len(_) == 1:
            numnumlist.append([_[0], _[0]])
        else:
            numnumlist.append([_[0], _[-1]])
    return numnumlist


def list_split(lst, x):
    """
    按指定长度拆分列表
    :param lst: [1,2,3]
    :param x: 1
    :return [[1],[2],[3]]
    """
    return [lst[i:i+x] for i in range(0, len(lst), x)]

def list_cmp(lst_1, lst_2):
    """
    对比两个列表 减少 遗留 新增
    :param lst_1: [1,2,3]
    :param lst_2: [3,4,5]
    :return [[1,2],[3],[4,5]]
    """
    return [_ for _ in lst_1 if _ not in lst_2], [_ for _ in lst_1 if _ in lst_2], [_ for _ in lst_2 if _ not in lst_1]


def dict_group(dic, lst):
    """
    将列表中的字典按1个或多个标题分组
    :param dic: [{"a":"a","b":"b"},{"a":"c","b":"d"}]
    :param lst: ["a","b"]
    :return {'a_b':[{"a":"a","b":"b"},{"a":"c","b":"d"}]}
    """
    gdic = {}
    for item in dic:
        key = '_'.join([str(item.get(line, 'None')) for line in lst])
        gdic.setdefault(key, [])
        gdic[key].append(item)
    return gdic


def dict_cmp(dic_1, dic_2, lst):
    """
    对比两个列表中字典 减少 遗留 新增
    :param dic_1: [{"a":"a","b":"b"},{"a":"c","b":"d"}]
    :param dic_2: [{"a":"c","b":"d"},{"a":"e","b":"f"}]
    :param lst: ["a","b"]
    :return [[{"a":"a","b":"b"}],[{"a":"c","b":"d"}],[{"a":"e","b":"f"}]]
    """
    ndic_1 = dict_group(dic_1, lst)
    ndic_2 = dict_group(dic_2, lst)
    lst_a, lst_b, lst_c = list_cmp(list(ndic_1.keys()), list(ndic_2.keys()))
    return [_ for k in lst_a for _ in ndic_1[k]], [_ for k in lst_b for _ in ndic_2[k]], [_ for k in lst_c for _ in ndic_2[k]]

def idn2xn(domain):
    """
    中文域名转英文
    :param domain: xxx.com
    :return 英文域名
    """
    try:
        return str(domain.encode('idna'), encoding='UTF-8')
    except:
        return 

def xn2idn(domain):
    """
    英文域名转中文
    :param domain: xxx.com
    :return 中文域名
    """
    try:
        return bytes(domain, encoding='UTF-8').decode('idna')
    except:
        return 

if __name__ == '__main__':
    pass

