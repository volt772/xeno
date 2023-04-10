#!/usr/bin/python3
# -*-coding:utf-8 -*-

import mysql.connector.pooling
from v2.databases import cf_msql, cv
from v2.helpers import log_maker

""" MySQL Connection 모듈
MySQL MySQLConnectionPool 사용
"""


class MSConnector:
    def __init__(self):
        self.dbconfig = {
            "host": cf_msql["db_host"],
            "port": cf_msql["db_port"],
            "user": cf_msql["db_user"],
            "password": cf_msql["db_pass"],
            "database": cf_msql["db_name"],
        }

        self.pool = self.create_pool()

    def create_pool(self):
        """POOL 생성"""
        pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name=cf_msql["db_pool_name"],
            pool_size=int(cf_msql["db_pool_size"]),
            pool_reset_session=True,
            **self.dbconfig
        )

        return pool

    def close(self, conn, cursor):
        """Connection 종료"""
        cursor.close()
        conn.close()

    def query(self, sql):
        """쿼리(Single)"""
        conn = self.pool.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)

        _data = cursor.fetchall()
        _cols = [i[0] for i in cursor.description]

        records = []
        if _data is not None:
            records = self.get_dict_all(_cols, _data)

        self.close(conn, cursor)
        return records

    def get_dict_all(self, cols, data):
        """쿼리 Row 생성"""
        record = []
        for row in data:
            record.append(dict(list(zip(cols, row))))

        return record


if __name__ == "__main__":
    msc = MSConnector()
