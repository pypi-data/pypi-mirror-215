#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import ruamel.yaml as yaml

def json2yaml(path,data,encoding='utf8'):
    ''''
    写入yaml文件
    :param path; yaml文件路径
    :param data
    '''
    with open(path, 'w', encoding=encoding) as f:
        yml = yaml.YAML()
        yml.indent(mapping=4, sequence=4, offset=4)
        yml.dump(data, f)

def yaml2json(path,encoding='utf8'):
    ''''
    读取yaml文件
    :param path: yaml文件路径
    :return 返回json
    '''
    with open(path, 'r',encoding=encoding) as f:
        data = yaml.load(f, Loader=yaml.Loader)
    return data