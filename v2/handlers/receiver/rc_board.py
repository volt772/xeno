#!/usr/bin/python3
# -*- coding: utf-8 -*-

from v2 import const as C
from v2.helpers import log_maker, utils, validator
from v2.models import _md_board

""" 게시판 알림 저장
새글, 댓글, 대댓글등 게시판에 관련된 액션이 발생하면,
알림서버에서 정보 수신 및 Redis에 큐로 적재한다.
"""


class BoardReceiveHandlerException(Exception):
    def __init__(self, msg=""):
        self.msg = msg
        log_maker.logging_default(log_type=C.Logger.RC_BOARD, msg=str(msg))

    def __str__(self):
        return self.msg


class BoardReceiveHandler:
    def __init__(self):
        pass

    def receive_board(self, data):
        """게시판 처리내용 수신"""
        if validator.data_is_empty(data):
            return False

        #: 수신자리스트 없으면 중지
        if validator.data_is_empty(data["to"]):
            return False

        #: 각 수신자용으로 큐데이터 생성
        bq_list = []
        for _to_addr in data["to"]:
            if utils.check_valid_user(_to_addr):
                _bq = {
                    "type": "mo_board",
                    "to": _to_addr,
                    "from": data.get("from", ""),
                    "content": data.get("content", ""),
                    "subject": data.get("subject", ""),
                    "board_id": data.get("board_id", 0),
                    "post_id": data.get("post_id", 0),
                    "comment_id": 0
                    if data["comment_id"] is None
                    else data["comment_id"],
                    "kind": data.get("kind", C.PostingKind.WRITE),
                    "count": data.get("count", 0),
                }

                bq_list.append(_bq)

                #: 로깅
                log_maker.logging_wms("board", _bq)

        _md_board.post_board(bq_list)


if __name__ == "__main__":
    brh = BoardReceiveHandler()
