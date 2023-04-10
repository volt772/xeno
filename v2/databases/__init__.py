#!/usr/bin/python3
# -*-coding:utf-8 -*-

from v2 import const as C
from v2.helpers import config_loader as _cf


#: MySQL 접속정보
cf_msql = _cf.get_config(C.ConfigKey.MYSQL)

#: Postgresql 접속정보
cf_psql = _cf.get_config(C.ConfigKey.PSQL)

#: Redis 접속정보
cf_redis = _cf.get_config(C.ConfigKey.REDIS)

#: 데이터 Value
cv = C.ConfigValue
