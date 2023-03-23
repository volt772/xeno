#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "/root/workspace/src/app-notify")

from v2 import const as C
from v2.helpers import utils
from v2.databases.db_redis import RDConnector

import os

""" sync_user_to_domain_path
- crontab에서 호출 (매일 새벽1시)
- 도메인 정보 수집기
- FCM 발송 대상 이메일주소를 수집하며, cron에 의해 실행 및
  /root/workspace/src/domain_list 내에 파일로 생성한다
"""

_rd = RDConnector()

USER_KEY = C.RedisKey.NOTI_USER

FCM_DOMAIN_PATH = "{0}/".format(C.Path.FCM_DOMAIN_LIST)

def sync_user_to_domain_path():
    """ Redis 사용자 데이터를 FCM 도메인 리스트에 파일로 생성한다"""
    conn = _rd.connection

    #: 로깅용 카운트
    sync_count = 0

    for the_file in os.listdir(FCM_DOMAIN_PATH):
        try:
            file_full_path = "{0}{1}".format(FCM_DOMAIN_PATH, the_file)
            if os.path.isfile(file_full_path):
                os.unlink(file_full_path)
        except Exception as e:
            pass
    
    for key in conn.scan_iter(USER_KEY + "*"):
        if key:
            email_key = key.decode("utf-8")
            domain = email_key.replace(USER_KEY, "").replace(":", ".")
            _path = "{0}{1}".format(FCM_DOMAIN_PATH, domain)

            if not os.path.isfile(_path):
                sync_count += 1
                with open(_path, "w") as fd:
                    fd.write(domain)
            else:
                pass

    #: 로깅
    print("{0}, [User Sync] {1} Users are Synchronized.".format(utils.get_logging_time(), sync_count))

if __name__ == "__main__":
    sync_user_to_domain_path()
