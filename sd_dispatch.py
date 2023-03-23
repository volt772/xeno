#!/usr/bin/python3
# -*- coding: utf-8 -*-

from v2 import const as C
from v2.helpers import log_maker, validator

from v2.models import _md_outsider

from v2.handlers.sender.sd_queue import SenderQueue
from v2.handlers.sender.sd_utils import SendUtilHandler
from v2.handlers.sender.outsiders import _rqwatcher, _webmail, _webhook, _puddlr, _caldav, _board, _eas

import traceback
import itertools 


""" SendDispatcher (메일 발송기)
- 메일 발송기
"""

_queue = SenderQueue()
_send_utils = SendUtilHandler()


class SendDispatcherException(Exception):

    def __init__(self, msg=''):
        self.msg = msg
        log_maker.logging_default(log_type = C.Logger.SD_DISPATCH, msg = str(msg))

    def __str__(self):
        return self.msg


class SendDispatcher:
    def __init__(self):
        pass

    def send_notification(self):
        """ 메일알림발송"""
        try:
            #: noti#queue#mails
            mqs = _queue.get_notidata(C.MAIL)
            for mq in mqs:
                if mq:
                    #: 일반 RQ 알림 발송
                    fcm_bundle = self.make_fcm_bundle(mq, C.MAIL)
                    if fcm_bundle:
						send()

            #: noti#queue#extras
            eqs = _queue.get_notidata(C.EXTRAS)
            for eq in eqs:
                if eq:
                    #: 네이티브 알림발송 (게시판, 전자결재, CalDAV)
                    send_type = eq[C.TYPE]
                    fcm_bundle = self.make_fcm_bundle(eq, send_type)
                    if fcm_bundle:
						send()

        except Exception as e:
            raise SendDispatcherException(str(e))
            pass

    def send_calendar(self, cq_list):
        """ 캘린더알림발송"""
		pass

    def make_fcm_bundle(self, _q, _type=C.MAIL):
        """ 기기정보 선별 및 기타 API 처리"""
        email = _q[C.TO]
        fcm_bundle = {}

		return {
			C.DEVICES : devices,
			C.EMAIL : email,
			C.EQ : _q
		}


        except Exception as e:
            raise SendDispatcherException(str(e))

        return fcm_bundle


if __name__ == "__main__":
    sd = SendDispatcher()
    sd.send_notification()
