#!/usr/bin/python3
# -*- coding: utf-8 -*-

import ast
import json

from v2 import const as C
from v2.handlers.sender.sd_queue import SenderQueue
from v2.handlers.sender.sd_utils import SendUtilHandler
from v2.helpers import fcm_info, log_maker
from v2.helpers import noti_launcher as _launcher
from v2.helpers import utils, validator

""" 메일 알림 발송
큐에 저장된 메일 관련 알림을 조건 검사후, 발송한다
"""

_queue = SenderQueue()
_send_utils = SendUtilHandler()


class RqWatcherHandlerException(Exception):
    def __init__(self, msg=""):
        self.msg = msg
        log_maker.logging_default(log_type=C.Logger.OS_RQWATCHER, msg=str(msg))

    def __str__(self):
        return self.msg


class RqWatcherHandler:
    def __init__(self):
        pass

    def make_notification(self, fcm_bundle):
        """알림발송 전 데이터 최종가공"""
        if validator.data_is_empty(fcm_bundle):
            return False

        rollback_list = {}

        mq = fcm_bundle["mq"]  #: 발송대상 메일 큐
        devices = fcm_bundle["devices"]  #: 기기 리스트 (Dict)
        email = fcm_bundle["email"]  #: 수신자 이메일주소
        host = fcm_bundle["au_host"]  #: 호스트

        #.... {중략} ...

        if fcm_data:
            for k, _ in devices.items():
                if "an_type" not in devices[k]:
                    break

                device_type = devices[k]["an_type"]

                self.do_push(
                    {
                        "device_type": device_type,
                        "fcm_data": fcm_data,
                        "device": devices[k],
                        "monit_msg": monit_msg,
                        "rollback_list": rollback_list,
                        "folder_kind": fcm_pack["kind"],
                        "fcm_type": fcm_pack["type"],
                        "email": email,
                        "host": host,
                        "view_kind": fcm_pack["view_kind"],
                    }
                )

    def do_push(self, noti_pack):
        """조건검사 및 FCM 발송"""
        if validator.data_is_empty(noti_pack):
            return False

        #: FCM 발송 Server Key
        fcm_server_key = fcm_server_url = ""

        #: FCM 발송데이터
        device_type = noti_pack["device_type"]
        fcm_data = noti_pack["fcm_data"]
        device = noti_pack["device"]
        email = noti_pack["email"]
        monit_msg = noti_pack["monit_msg"]
        rollback_list = noti_pack["rollback_list"]
        host = noti_pack["host"]
        view_kind = noti_pack["view_kind"]

        #: 메일 발송여부 구분 (하이브리드일 경우에만 사용)
        folder_kind = noti_pack["folder_kind"]
        fcm_type = noti_pack["fcm_type"]

        #: 발송여부 (전체, 폴더 및 방해시간)
        is_sendable = True
        is_sendable_folder = True
        is_sendable_time = True

        #: 발송 장치 구분
        device_type = _send_utils.select_device_type(device["an_uuid"])

        #: 인덱스 언어설정
        lang = device["au_lang"] if "au_lang" in device else "kr"

        if validator.string_is_empty(lang):
            lang = "kr"

        #.... {중략} ...

        if is_sendable_folder and is_sendable_time and is_sendable:
            os_type = device["an_type"]
            if os_type == C.OSKind.ANDROID:
                #: Android 발송
                fcm_data["noti"]["unread_count"] = badge_count if badge_count > 0 else 0

                m_data = fcm_data["noti"]
                f_data = m_data["noti_0"]

                #: Folder ID 예외
                folder_id = 0
                if (
                    view_kind == C.MailViewKind.NORMAL
                    and not validator.string_is_empty(f_data["kind"])
                ):
                    folder_id = int(f_data["kind"])

                payload = {
                    "to": fcm_to_token,
                    "priority": "high",
                    "data": {
                        "type": f_data["type"],
                        "content": f_data["title"],
                        "subject": f_data["from"],
                        "ref_url": f_data["ref_url"],
                        "view_kind": view_kind,
                        "count": m_data["unread_count"],
                        "to": f_data["to"],
                        "folder_id": folder_id,
                    },
                }
            elif os_type == C.OSKind.IOS:
                #: iOS 발송
                ios_noti = {
                    "title": fcm_data["noti"]["noti_0"]["from"],
                    "body": fcm_data["noti"]["noti_0"]["title"],
                    "sound": "default",
                    "vibrate": True,
                }

                if badge_count and badge_count > 0:
                    ios_noti["badge"] = badge_count

                if device_type == C.PushType.HYBRID:
                    #: iOS Hybrid
                    payload = {
                        "to": fcm_to_token,
                        "priority": "high",
                        "data": fcm_data,
                        "notification": ios_noti,
                    }
                else:
                    #: iOS Native
                    ios_noti["data"] = fcm_data["noti"]["noti_0"]
                    payload = {
                        "to": fcm_to_token,
                        "priority": "high",
                        "notification": ios_noti,
                    }

            else:
                payload = {}

            headers = {
                "Authorization": fcm_server_key,
                "Content-Type": "application/json",
                "cache-control": "no-cache",
            }

            #: FCM 전송
            try:
                log_maker.logging_monit(os_type, device_type, monit_msg)
                _launcher.post_fcm(
                    fcm_server_url, "POST", C.RemotePath.FCM_SEND, payload, headers
                )
            except Exception as e:
                _queue.put_exception_data(
                    ast.literal_eval(json.dumps(rollback_list[0]))
                )
                log_maker.logging_default(log_type=C.Logger.OS_RQWATCHER, msg=str(e))


if __name__ == "__main__":
    rwh = RqWatcherHandler()
