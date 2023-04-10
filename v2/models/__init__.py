#!/usr/bin/python3
# -*-coding:utf-8 -*-

from v2.models.md_board import BoardModel
from v2.models.md_mail import MailModel
from v2.models.md_outsider import OutsiderModel
from v2.models.md_user_psql import UserPsqlModel
from v2.models.md_user_redis import UserRedisModel

#: 이메일 모델
_md_mail = MailModel()

#: 사용자 모델 (Postgresql)
_md_user_psql = UserPsqlModel()

#: 사용자 모델 (Redis)
_md_user_redis = UserRedisModel()

#: 외부 웹훅
_md_outsider = OutsiderModel()

#: 게시판 모델
_md_board = BoardModel()