#!/usr/bin/python3
# -*- coding: utf-8 -*-

import emoji
from v2 import const as C
from v2.handlers.sender.sd_utils import SendUtilHandler
from v2.helpers import fcm_info, log_maker
from v2.helpers import noti_launcher as _launcher
from v2.helpers import utils, validator

""" 게시판 알림 발송
큐에 저장된 게시판 관련 알림을 조건 검사후, 발송한다
"""

_send_utils = SendUtilHandler()


class BoardHandlerException(Exception):
    def __init__(self, msg=""):
        self.msg = msg
        log_maker.logging_default(log_type=C.Logger.OS_BOARD, msg=str(msg))

    def __str__(self):
        return self.msg


class BoardHandler:
    def __init__(self):
        pass

    def check_disturb_time(self, _time):
        """조건1 : 방해시간"""
        return _send_utils.check_noti_time(_time)

    def check_all_noti(self, _all):
        """조건2 : 전체설정"""
        if "board" in _all:
            return bool(_all["board"])

    def check_excluded_board_number(self, board_id, folders):
        """조건3 : 예외폴더"""
        return True if board_id not in folders else False

    def check_tail_types(self, notifies, post_kind):
        """조건4 : 새글, 답글, 댓글 여부"""
        if post_kind == C.PostingKind.REPLY:
            #: 답글 : reply 값 검사
            return bool(notifies["reply"])
        elif post_kind == C.PostingKind.COMMENT:
            #: 댓글 : commnet 값 검사
            return bool(notifies["comment"])
        else:
            #: 새글 : 검사 없음
            return True

    def post_board(self, bq):
        """게시판 발송"""
        if validator.data_is_empty(bq):
            return False

        email = bq["email"]
        queue = bq["eq"]
        devices = bq["devices"]

        #: 게시판 발송여부 설정검사
        for _, _device in devices.items():
            #: 방해시간검사
            is_sendable_time = self.check_disturb_time(_device["au_time"])
            if not is_sendable_time:
                continue

            #: 전체발송여부검사
            is_sendable_board = self.check_all_noti(_device["au_all"])
            if not is_sendable_board:
                continue

            #: 예외폴더검사
            is_sendable_folder = self.check_excluded_board_number(
                queue["board_id"], _device["au_board"]["excludeFolders"]
            )
            if not is_sendable_folder:
                continue

            #: 새글, 댓글 ,답글 검사
            is_sendable_tail = self.check_tail_types(
                _device["au_board"]["notifyToMe"], queue["kind"]
            )
            if not is_sendable_tail:
                continue

            try:
                payload = {}

                #: 발송 데이터 Pack
                fcm_pack = {
                    "type": "board",
                    "content": utils.get_surrogatepass_str(queue["content"]),
                    "subject": utils.get_surrogatepass_str(queue["subject"]),
                    "board_id": queue["board_id"],
                    "post_id": queue["post_id"],
                    "comment_id": queue["comment_id"],
                    "count": queue["count"],
                }

                payload = {
                    "to": _device["an_token"],
                    "priority": "high",
                }

                if _device["an_type"] == C.OSKind.ANDROID:
                    #: Android Payload
                    payload["data"] = fcm_pack

                elif _device["an_type"] == C.OSKind.IOS:
                    #: iOS Payload
                    payload["notification"] = {
                        "title": fcm_pack["subject"],
                        "body": fcm_pack["content"],
                        "sound": "default",
                        "vibrate": True,
                        "data": fcm_pack,
                        "badge": fcm_pack["count"],
                    }

                #: Headers
                headers = {
                    "Authorization": fcm_info.MOBILE_MAILPLUG_NATIVE_SERVER_KEY(),
                    "Content-Type": "application/json",
                    "cache-control": "no-cache",
                }

                #: 로그메세지
                abbr_title = utils.abbreviate_msg(30, fcm_pack["content"])
                _launcher.post_fcm(
                    fcm_info.MOBILE_MAILPLUG_NATIVE_SERVER_URL(),
                    "POST",
                    C.RemotePath.FCM_SEND,
                    payload,
                    headers,
                )

                #: 로깅
                log_maker.logging_extras(
                    emoji.emojize(":clipboard:"),
                    "board",
                    email,
                    fcm_pack["subject"],
                    abbr_title,
                )

            except Exception as e:
                raise BoardHandlerException(str(e))


if __name__ == "__main__":
    bh = BoardHandler()
