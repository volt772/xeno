#!/usr/bin/python3
# -*-coding:utf-8 -*-

from v2.handlers.receiver.rc_board import BoardReceiveHandler
from v2.handlers.receiver.rc_mail import MailReceiveHandler
from v2.handlers.receiver.rc_outsider import OutsiderReceiveHandler
from v2.handlers.receiver.rc_user import UserReceiveHandler

#: 이메일 핸들러
_mail = MailReceiveHandler()

#: 사용자 핸들러
_user = UserReceiveHandler()

#: 웹훅 핸들러
_outsider = OutsiderReceiveHandler()

#: 게시판 핸들러
_board = BoardReceiveHandler()