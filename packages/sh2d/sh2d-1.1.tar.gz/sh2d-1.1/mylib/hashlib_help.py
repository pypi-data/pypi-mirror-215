#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import hashlib


def file2md5(_file):
    ''''
    获取文件md5
    :param _file: 文件路径
    '''
    with open(_file, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        return md5obj.hexdigest()


def str2md5(_str, encoding='utf8'):
    ''''
    获取字符串md5
    :param _str: 字符串
    '''
    return hashlib.md5(_str.encode(encoding)).hexdigest()


def str2sha256(_str, encoding='utf8'):
    ''''
    获取字符串sha256
    :param _str: 字符串
    '''
    return hashlib.sha256(_str.encode(encoding)).hexdigest()
