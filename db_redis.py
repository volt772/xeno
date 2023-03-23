#!/usr/bin/python3
# -*-coding:utf-8 -*-

import redis
import time
import json
import ast

import unittest

from v2.helpers import utils, log_maker
from v2.databases import cf_redis, cv

""" RDConnector(데이터베이스 처리)
- Redis ConnectionPool 사용
"""


class RDConnector:
    def __init__(self):
        """ Redis Connector"""
        self._connection = None
        self.create_pool()

    @property    
    def connection(self):
        """ Property Connection """
        return self._connection

    def create_pool(self):
        """ Make Connection Pool """

        pool = redis.ConnectionPool(
            host = cf_redis[cv.DB_HOST],
            port = cf_redis[cv.DB_PORT], 
            db = cf_redis[cv.DB_NAME], 
            password = cf_redis[cv.DB_PASS],
            socket_timeout = int(cf_redis[cv.DB_TIMEOUT])
        )

        self._connection = redis.Redis(connection_pool=pool)

        log_maker.logging_database(
            msg = "Redis Pool Created : {0}".format(str(self._connection))
        )


if __name__ == "__main__":
    rdc = RDConnector()
