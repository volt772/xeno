#!/usr/bin/python3
# -*- coding: utf-8 -*-

import emoji
from v2 import const as C
from v2.databases.db_psql import PGConnector
from v2.helpers import log_maker, utils, validator
from v2.models.md_user_redis import UserRedisModel


""" 사용자 처리기
사용자가 모바일 및 기타 알림받을 엔드포인트에서 로그인하면 알림서버에 UUID등 고유번호를 등록하며,
차후에 이 고유번호를 가지고 FCM 발송이 이루어진다.
반대로 해제도 가능하다.
"""

_pg = PGConnector()

_urm = UserRedisModel()


class UserPsqlModelException(Exception):
    def __init__(self, msg=""):
        self.msg = msg
        log_maker.logging_default(log_type=C.Logger.MD_USER_PSQL, msg=str(msg))

    def __str__(self):
        return self.msg


class UserPsqlModel:
    def __init__(self):
        pass

    def put_user_from_mobile(self, an_email, data):
        """
        * 신규데이터 생성 (사용자로그인)
        * 기존 동일기기에 대한 데이터 존재시, 삭제 후, 재생성
        * 네이티브 기기에 한함
        """
        if validator.data_is_empty(data):
            return False

        #: 앱종류
        app_kind = data.get("appKind", "")

        #: 기본 설정값 지정
        if app_kind == "task":
            settings = {"host": data["host"]}
        else:
            settings = {
                "host": data["host"],
                "au_time": [],
                "au_mail": [],
                "au_eas": [],
                "au_board": {
                    "excludeFolders": [],
                    "notifyToMe": {"comment": 0, "reply": 0},
                },
                "au_cal": [],
                "au_all": {"mail": 1, "eas": 1, "board": 1, "cal": 1},
            }

        an_uuid = utils.device_uuid_maker(data["uuid"], data.get("appKind", ""))

        if not an_uuid:
            return False

        user_list = [
            {
                "an_email": an_email,
                "an_uuid": an_uuid,
                "an_token": data["token"],
                "an_type": data["osKind"],
                "an_data": settings,
            }
        ]

        return self.put_user(user_list)

    def get_users(self, nu_email):
        """
        * 이메일기준 기기정보 가져오기
        """
        return _pg.fetch_all(
            "SELECT * FROM noti_user WHERE nu_email = '{0}'".format(nu_email)
        )

    def get_users_by_uuid(self, nu_email, nu_uuid):
        """
        * 이메일, UUID 기준 기기정보 가져오기
        """
        nu_data = _pg.fetch_one(
            """
            SELECT nu_data
            FROM noti_user
            WHERE nu_email = '{0}'
            AND nu_uuid = '{1}'""".format(
                nu_email, nu_uuid
            )
        )

        if not validator.data_is_empty(nu_data):
            return nu_data["nu_data"]

    def del_dbs(self, data, is_all):
        """
        * 사용자정보삭제(사용자로그아웃)
        * email, uuid 조회 후, 삭제
        * Redis갱신 위해, 잔여데이터 반환
        """
        if validator.data_is_empty(data):
            return False

        db_res = []
        an_email = data.get("an_email", "")
        an_uuid = data.get("an_uuid", "")
        an_type = data.get("an_type", "")

        if not is_all:
            #: UUID 검사해서 삭제
            if not validator.string_is_empty(an_email, an_uuid, an_type):
                try:
                    _pg.execute(
                        """
                        DELETE FROM noti_user
                        WHERE nu_email='{0}' AND nu_uuid='{1}'""".format(
                            an_email, an_uuid
                        )
                    )

                except Exception:
                    db_res = False
        else:
            #: 전체삭제
            if not validator.string_is_empty(an_email):
                try:
                    _pg.execute(
                        """
                        DELETE FROM noti_user
                        WHERE nu_email='{0}'
                        AND nu_type != 'WEBHOOK'""".format(
                            an_email
                        )
                    )
                except Exception:
                    db_res = False

        result = _pg.fetch_all(
            "SELECT * FROM noti_user WHERE nu_email = '{0}'".format(an_email)
        )

        if not validator.data_is_empty(result):
            db_res = result

        return db_res

if __name__ == "__main__":
    upm = UserPsqlModel()
