#!/usr/bin/python3
# -*- coding: utf-8 -*-

from v2 import const as C
from v2.helpers import log_maker

from v2.handlers.receiver import _mail, _calendar, _domain, _user, _outsider, _board, _eas

""" 
라우팅 받은 데이터를 각 핸들러로 전달
- main과 각 handler간 bridge 역할
- 알림데이터, 사용자데이터 등등
"""


class XenoException(Exception):

    def __init__(self, msg=""):
        self.msg = msg
        log_maker.logging_default(
            log_type = C.Logger.XENO,
            msg = str(msg),
            sentry = False,
            err = None
        )

    def __str__(self):
        return self.msg

def distributor(route, data, ip):
    """ 라우팅 분배 """
    ep = C.EndPoint
    if route is ep.MAIL:
        mail(data, ip)
    elif route is ep.USER_LOGIN:
        user_login(data, ip)
    elif route is ep.USER_LOGOUT:
        user_logout(data)
    elif route is ep.OUTSIDER:
        outsider(data)
    elif route is ep.MO_BOARD:
        board(data)
    elif route is ep.MO_SETTING:
        return setting(data)
    else:
        raise XenoException("out of range for routing")
        

def mail(data, ip):
    """ 이메일"""
    if data and ip:
        _mail.receive_noti(data, ip) 

def user_login(data, ip):
    """ 사용자 로그인"""
    if data:
        _user.receive_put_user(data, ip) 

def user_logout(data):
    """ 사용자 로그아웃 알림"""
    if data:
        _user.receive_notify_for_logout(data) 

def outsider(data):
    """ 웹훅"""
    if data:
        _outsider.receive_webhook(data) 

def board(data):
    """ 게시판"""
    if data:
        _board.receive_board(data)

def setting(data):
    """ 설정 (네이티브 전용)"""
    if data:
        return _user.receive_mobile_user_setting(data)