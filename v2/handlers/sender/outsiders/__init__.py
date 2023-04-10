#!/usr/bin/python3
# -*-coding:utf-8 -*-

from v2.handlers.sender.outsiders.os_board import BoardHandler
from v2.handlers.sender.outsiders.os_rqwatcher import RqWatcherHandler
from v2.handlers.sender.outsiders.os_webhook import WebHookHandler

#: RQ Watcher 처리기
_rqwatcher = RqWatcherHandler()

#: WebHook 처리기
_webhook = WebHookHandler()

#: 게시판 처리기
_board = BoardHandler()