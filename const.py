#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" Description
상수 모음
- 각종 상수 
- Enum Class
- 에러코드 정의
"""

from enum import Enum

""" consts (상수모음)
"""
# A
ADD = "add"
AN_DATA = "an_data"

# B
BOARD = "board"
BODY = "body"

# C 
CAL = "cal"
CALDAV = "caldav"

# D
DATA = "data"
DATE = "date"

# E 
EAS = "eas"
EMAIL = "email"

# F 
FROM = "from"
FCM_DATA = "fcm_data"

# G
# H
HOOK_TYPE = "hook_type"
HOST = "host"

# I
IP = "ip"
IS_TEST = "is_test"

# J
# K
KEY = "key"
KIND = "kind"

# L
LOG = "log"
LOG_MSG = "log_msg"

# M
MAIL = "mail"
MAIL_FOLDER_KIND = "mail_folder_kind" 

# N
NAMES = "names"
NC_DATA = "nc_data"

# O
ORGAN1 = "organ1"
ORIG_DEVICE = "orig_device"

# P
POST = "post"
POST_ID = "post_id"

# Q
# R
REF_URL = "ref_url"
REPEAT_LIST = "repeat_list"

# S
SAVED_TIME = "saved_time"
SET = "set"

# T
TEXT = "text"
TITLE = "title"

# U
UNICODE_ESCAPE = "unicode-escape"
UNKNOWN = "UNKNOWN"

# V
VIEW_KIND = "view_kind"
VIBRATE = "vibrate"

# W 
WEBHOOK = "WEBHOOK"
WEBMAIL_HOST = "webmail_host"

# X
X_FORWARD_FOR = "X-Forward-For"

# Y 
# Z 

class MailViewKind():
    """ 메일View타입"""
    NORMAL = "normal"
    APPROVAL = "approval"

class RedisKey():
    """ Redis Key"""
    NOTI_USER = "noti#user#"
    NOTI_USER_EXTRAS = "noti#user#extras#"

class EndPoint():
    """ 라우팅 분배키"""
    MAIL = "mail"
    CALENDAR = "calendar"

class ConfigKey():
    """ 설정 키"""
    APP = "app"
    QUEUE = "queue"

class ConfigValue():
    """ 설정 값"""
    API_KEY = "api_key"
    API_URL = "api_url"

class Logger():
    """ 로그"""
    USER = "user"
    PUDDLR = "puddlr"

    FILE = {
        USER : "user.log",
        PUDDLR : "puddlr.log",
    }

    RC_BOARD = "rc_board"
    RC_EAS = "rc_eas"

class OSKind():
    """ OS 타입"""
    ANDROID = "ANDROID"
    IOS = "IOS"

class PushType():
    """ 발송 타입"""
    HYBRID = "hybrid"
    NATIVE = "native"
    NOTI_KIND = {
        "kr_mail" : u"[메일] ",
        "kr_eas" : u"[전자결재] ",
        "kr_cal" : u"[캘린더] ",
        "en_mail" : u"[Mail] ",
        "en_eas" : u"[Approval] ",
        "en_cal" : u"[Calendar] ",
    }

class FCM():
    """ FCM Keys"""
    AU_TIME = "au_time"
    NOTI = "noti"
    TIME = "time" 

class APISendType():
    """ 외부 API 발송 타입"""
    CURL = "curl"
    MSQL = "msql"

class ResponseCode():
    """ Response Codes"""
    SUCCESS = 500000

    COMM_ERROR = 510000
    NO_DATA = 510001