#!/usr/bin/python3
# -*-coding:utf-8 -*-

import redis
from v2.databases import cf_redis, cv
from v2.helpers import log_maker

""" Redis Connection 모듈
RDConnector(데이터베이스 처리)

- Redis ConnectionPool 사용
"""

class RDConnector:
    def __init__(self):
        """Redis Connector"""
        self._connection = None
        self.create_pool()

    @property
    def connection(self):
        """Property Connection"""
        return self._connection

    def create_pool(self):
        """Make Connection Pool"""

        pool = redis.ConnectionPool(
            host=cf_redis["db_host"],
            port=cf_redis["db_port"],
            db=cf_redis["db_name"],
            password=cf_redis["db_pass"],
            socket_timeout=int(cf_redis["db_timeout"]),
        )

        self._connection = redis.Redis(connection_pool=pool)


if __name__ == "__main__":
    rdc = RDConnector()
