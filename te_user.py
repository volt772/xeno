#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import traceback
import unittest

from v2.handlers.receiver import _user
from time import sleep

""" UserTester
- Tester 사용자
"""

class UserTester(unittest.TestCase):

    ip = "1.1.1.1"

    start_time = 0
    end_time = 0

    def setUp(self):
        self.__class__.start_time = time.time()

    def tearDown(self):
        self.__class__.end_time = time.time() - self.__class__.start_time
        print(" >>>>>>>>>>> Elapsed Seconds : {0}".format(self.__class__.end_time))

    def test_login_hybrid(self):
        """ [101] 하이브리드 로그인"""
        print("""
        ===========================================================================================
            [101] 하이브리드 로그인
            * 테스트 LG폰에서 '하이브리드'로 로그인한다
        ===========================================================================================
        """)

        data = [{u'an_email': u'hnjeong@b53.myplug.kr', \
        u'an_type': u'ANDROID', \
        u'an_data': {u'au_all': u'[1,1,1]', u'au_time': u'[]', u'au_mail': u'[]', u'au_eas': u'[]', \
        u'host': u'mb102', u'au_cal': u'[]', u'au_eas_pc': []}, \
        u'an_uuid': u'0000-4933-3', \
        u'an_token': u'dLzqf3Flq-U:AP'}]

        _user.receive_put_user(data, self.__class__.ip)

