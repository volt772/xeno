#!/usr/bin/python3
# -*- coding: utf-8 -*-

from v2 import const as C
from v2.helpers import utils, log_maker, validator

from v2.databases.db_psql import PGConnector
from v2.models.md_user_redis import UserRedisModel


""" UserPostgresModel (사용자 데이터 처리기)
- Postgresql
"""

_pg = PGConnector()

_urm = UserRedisModel()



class UserPsqlModelException(Exception):

    def __init__(self, msg=''):
        self.msg = msg
        log_maker.logging_default(log_type = C.Logger.MD_USER_PSQL, msg = str(msg))

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

        #: 기본 설정값 지정
        settings = {
            C.HOST : data[C.HOST],
            C.AU_TIME : [],
            C.AU_MAIL : [],
            C.AU_EAS : [],
            C.AU_BOARD : { C.EXCLUDE_FOLDERS : [], C.NOTIFY_TO_ME : { C.COMMENT : 0, C.REPLY : 0 } },
            C.AU_CAL : [],
            C.AU_ALL : { C.MAIL : 1, C.EAS : 1, C.BOARD : 1, C.CAL : 1 }
        }

        user_list = [{
            C.AN_EMAIL : an_email,
            C.AN_UUID : "{0}{1}".format(data[C.UUID], C.NATIVE_POSTFIX),
            C.AN_TOKEN : data[C.TOKEN],
            C.AN_TYPE : data[C.OS_KIND],
            C.AN_DATA : settings
        }]

        return self.put_user(user_list)

    def put_user_setting_from_mobile(self, settings):
        """
        * 설정저장 (사용자로그인)
        * 네이티브 기기에 한함
        """
        if validator.data_is_empty(settings):
            return False

        #: 이메일키 
        nu_email = settings[C.AN_EMAIL]
        nu_uuid = settings[C.AN_UUID]

        #: 기존 설정정보
        user_prefs = self.get_users_by_uuid(nu_email, nu_uuid)

        #: 설정 nu_data 생성
        all_setting = settings[C.AU_ALL]

        nu_data = {
            C.HOST : settings[C.HOST],
            C.AU_TIME : settings[C.AU_TIME],
            C.AU_MAIL : settings[C.AU_MAIL],
            C.AU_EAS : settings[C.AU_EAS],
            C.AU_BOARD : settings[C.AU_BOARD],
            C.AU_CAL : settings[C.AU_CAL],
            C.AU_ALL : {
                C.MAIL : all_setting[C.MAIL], 
                C.EAS : all_setting[C.EAS], 
                C.BOARD : all_setting[C.BOARD], 
                C.CAL : all_setting[C.CAL]
            }
        }

        self.update_user_settings(nu_email, nu_data, C.PushType.NATIVE, nu_uuid)

        return self.get_users(nu_email)



if __name__ == "__main__":
    upm = UserPsqlModel()  
