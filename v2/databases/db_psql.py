#!/usr/bin/python3
# -*-coding:utf-8 -*-

import psycopg2
from psycopg2 import pool
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from v2.databases import cf_psql, cv
from v2.helpers import log_maker

""" PostgreSQL Connection 모듈
postgresql ThreadedConnectionPool 사용

- 참고 : https://pynative.com/psycopg2-python-postgresql-connection-pooling/
"""


class PGConnector:
    def __init__(self):
        self.threaded_postgreSQL_pool = None
        self.create_pool()

    def get_conn(self):
        """Connection 요청"""
        ps_connection = self.threaded_postgreSQL_pool.getconn()
        ps_connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        if ps_connection:
            ps_cursor = ps_connection.cursor()

        return ps_connection, ps_cursor

    def put_conn(self, ps_connection):
        """Connection 반환"""
        self.threaded_postgreSQL_pool.putconn(ps_connection)

    def destroy(self):
        """모든 Connection 종료"""
        if self.threaded_postgreSQL_pool:
            self.threaded_postgreSQL_pool.closeall

    def create_pool(self):
        """Database 연결 및 ConnectionPool 생성"""
        self.threaded_postgreSQL_pool = psycopg2.pool.ThreadedConnectionPool(
            int(cf_psql["db_min_connection"]),
            int(cf_psql["db_max_connection"]),
            user=cf_psql["db_user"],
            password=cf_psql["db_pass"],
            host=cf_psql["db_host"],
            port=cf_psql["db_port"],
            database=cf_psql["db_name"],
        )

    def fetch_one(self, query):
        """쿼리(Single)"""
        ps_connection, ps_cursor = self.get_conn()
        ps_cursor.execute(query)
        _data = ps_cursor.fetchone()
        _cols = [desc[0] for desc in ps_cursor.description]

        record = []
        if _data is not None:
            record = self.get_dict_one(_cols, _data)[0]

        ps_cursor.close()
        self.put_conn(ps_connection)
        return record

    def fetch_all(self, query):
        """쿼리(Multi)"""
        ps_connection, ps_cursor = self.get_conn()
        ps_cursor.execute(query)
        _data = ps_cursor.fetchall()
        _cols = [desc[0] for desc in ps_cursor.description]

        records = []
        if _data is not None:
            records = self.get_dict_all(_cols, _data)

        self.put_conn(ps_connection)
        return records

    def execute(self, query):
        """쿼리(Raw)"""
        ps_connection, ps_cursor = self.get_conn()
        ps_cursor.execute(query)
        rowcount = ps_cursor.rowcount
        ps_cursor.close()
        self.put_conn(ps_connection)
        return rowcount

    def get_dict_all(self, cols, data):
        """쿼리 Row 생성"""
        record = []
        for row in data:
            record.append(dict(list(zip(cols, row))))

        return record

    def get_dict_one(self, cols, data):
        """쿼리 Row 생성"""
        rows = []
        record = []
        for row in data:
            rows.append(row)

        record.append(dict(list(zip(cols, rows))))
        return record


if __name__ == "__main__":
    pgc = PGConnector()
    pgc.execute("select * from noti_user")
