#!/usr/bin/python3
# -*- coding: utf-8 -*-

from v2 import const as C
from v2.handlers.sender.outsiders import (
    _board,
    _rqwatcher,
    _webhook,
)
from v2.handlers.sender.sd_queue import SenderQueue
from v2.handlers.sender.sd_utils import SendUtilHandler
from v2.helpers import log_maker
from v2.models import _md_outsider

""" 알림 발송기
큐에서 알림을 뺀 후, 상황에 맞게 발송대상 선별 및 조건검사를 진행한다.
1단계 : 사용자 정보를 Redis에서 조회한다
2단계 : 사용자가 설정한 알림 수신조건을 검사한다
3단계 : 예외처리가 되어있는 사용자인지 검사한다
4단계 : 발송한다.
"""

_queue = SenderQueue()
_send_utils = SendUtilHandler()


class SendDispatcherException(Exception):
    def __init__(self, msg=""):
        self.msg = msg
        log_maker.logging_default(log_type=C.Logger.SD_DISPATCH, msg=str(msg))

    def __str__(self):
        return self.msg


class SendDispatcher:
    def __init__(self):
        pass

    def send_notification(self):
        """메일알림발송"""
        try:
            #: 메일 알림 발송
            mqs = _queue.get_notidata("mail")
            for mq in mqs:
                if mq:
                    #: 일반 RQ 알림 발송
                    fcm_bundle = self.make_fcm_bundle(mq, "mail")
                    if fcm_bundle:
                        _rqwatcher.make_notification(fcm_bundle)

            #: 게시판 알림 발송
            eqs = _queue.get_notidata("extras")
            for eq in eqs:
                if eq:
                    send_type = eq["type"]
                    fcm_bundle = self.make_fcm_bundle(eq, send_type)
                    if fcm_bundle:
                        if send_type == "mo_board":
                            #: 게시판
                            _board.post_board(fcm_bundle)
                        else:
                            continue


        except Exception as e:
            raise SendDispatcherException(str(e))

    def send_calendar(self, cq_list):
        """캘린더알림발송"""
        
        try:
            pass
            #...{중략}...
        except Exception as e:
            raise SendDispatcherException(str(e))

    def make_fcm_bundle(self, _q, _type="mail"):
        """기기정보 선별 및 기타 API 처리"""
        email = _q["to"]
        fcm_bundle = {}

        try:
            #: 기기리스트 조회
            devices = _send_utils.do_check_device_list(email)

            if _type == "mail":

                #: 특정 PASS 처리 : 리스트 생성
                _, pass_type = _send_utils.get_pass_list()

                #: 특정 PASS 처리 : 발송 조건검사 (도메인 및 IP)
                is_pass_domain = _send_utils.check_pass_for_domain(email)
                is_pass_ip = _send_utils.check_pass_for_ip(_q["ip"])

                send_to_outsider = True if is_pass_domain or is_pass_ip else False

                #...{중략}...

            #: 기기정보 존재시 실행
            if devices:
                    #...{중략}...
                    fcm_bundle = {
                        "devices": devices,
                        "email": email,
                        "mq": _q,
                        "log_msg": log_msg,
                        "au_host": au_host,
                    }
        except Exception as e:
            raise SendDispatcherException(str(e))

        return fcm_bundle

    def get_device_only_mo(self, devices):
        """기기선출
        - 네이티브 기기만 선출 (통합메일앱)
        """
        purge_uuids_extras = []
        for _key in devices.keys():
            if not _key.endswith(C.PostFix.NATIVE_POSTFIX):
                purge_uuids_extras.append(_key)

        #: 기기리스트 재정리 (네이티브만 선별)
        for _purge in purge_uuids_extras:
            del devices[_purge]

        return devices


if __name__ == "__main__":
    sd = SendDispatcher()
    sd.send_notification()
