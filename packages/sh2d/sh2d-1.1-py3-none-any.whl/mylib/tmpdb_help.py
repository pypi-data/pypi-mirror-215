#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
from .sqlite_help import sqliteDB
from .ipaddress_help import ip2num


class tmpDB():

    def __init__(self, dbname=":memory:"):
        """
        初始化函数，创建数据库连接
        :param dbnmae: 传入数据库名称或数据库文件路径，eg: test.db 或 :memory:
        """
        if not os.path.exists(dbname) or dbname == ":memory:":
            self.db = sqliteDB(
                dbname, [
                    'CREATE TABLE tmp1 (key TEXT NOT NULL,value TEXT NOT NULL);',
                    'CREATE TABLE tmp2 (start INT NOT NULL,end INT NOT NULL,value TEXT NOT NULL);',
                    ])
        else:
            self.db = sqliteDB(dbname)

    def get(self, key):
        result = self.db.get("select value from tmp1 where key=?", [key, ])
        if len(result) == 0:
            return 
        else:
            return result[0][0]

    def get_ip(self, ip):
        result = self.db.get("select value from tmp2 where start <= ? and ? <= end", [ip2num(ip),ip2num(ip) ])
        if len(result) == 0:
            return []
        else:
            return [_[0] for _ in result]

    def set(self, key, value):
        result = self.db.get("select value from tmp1 where key=?", [key, ])
        if len(result) == 0:
            return self.db.set('INSERT INTO tmp1 (key,value) VALUES (?,?)', [key, value])
        else:
            return self.db.set('UPDATE tmp1 set value = ? where key=?', [value, key])

    def sets(self, kv=[]):
        return self.db.set('INSERT INTO tmp1 (key,value) VALUES (?,?)', kv,many=True)

    def set_ip(self, start_ip,end_ip, value):
        result = self.db.get("select value from tmp2 where start=? and end=? ", [ip2num(start_ip),ip2num(end_ip)])
        if len(result) == 0:
            return self.db.set('INSERT INTO tmp2 (start,end, value) VALUES (?,?,?)', [ip2num(start_ip),ip2num(end_ip), value])
        else:
            return self.db.set('UPDATE tmp2 set value = ? where start=? and end=?', [value, ip2num(start_ip),ip2num(end_ip)])
    
    def set_ips(self, kv = []):
        kv = [[ip2num(start_ip),ip2num(end_ip),value] for start_ip,end_ip,value in kv]

        return self.db.set('INSERT INTO tmp2 (start,end, value) VALUES (?,?,?)', kv,many=True)

    def remove(self, key):
        return self.db.set("DELETE from tmp1 where key=?", [key, ])

    def remove_ip(self, start_ip,end_ip):
        return self.db.set("DELETE from tmp2 where start=? and end=? ", [ip2num(start_ip),ip2num(end_ip) ])

if __name__ == '__main__':
    db = tmpDB()
    db.set('a', 'a')
    db.set('a', 'b')
    db.set('c', 'c')
    print(db.get('a'))
    print(db.get('b'))
    print(db.get('c'))
    db.remove('c')
    print(db.get('c'))
