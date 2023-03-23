#!/usr/bin/python3 
# -*- coding: utf-8 -*-

from v2 import const as C
from v2.helpers import utils, noti_launcher, responser, validator, log_maker

import os
import ast
import json

from v2.models import _md_user_psql
from v2.models import _md_user_redis

""" UserReceiveHandler (유저 수신기)
- 사용자 정보 처리 (로그인, 로그아웃) 
"""

# TMP 도메인 경로
TMP_DOMAIN_PATH = C.Path.TMP_DOMAIN_LIST

# Responser
_resp = responser.Responser()


class UserReceiveHandlerException(Exception):

    def __init__(self, msg=''):
        self.msg = msg
        log_maker.logging_default(log_type = C.Logger.RC_USER, msg = str(msg))

    def __str__(self):
        return self.msg


class UserReceiveHandler:
    def __init__(self):
        pass

    """
    사용자 IN / OUT 처리
    * 신규 네이티브 기기
    """
    def receive_mobile_user_login(self, data):
        """ 사용자 로그인(네이티브 기기 전용)"""
        if validator.data_is_empty(data):
            return _resp.Resp(C.ResponseCode.NO_DATA)

        #: 필수값 검증
        if not validator.login_data_is_valid(data):
            return _resp.Resp(C.ResponseCode.DATA_INSUFFICIENT)

        #: OS종류 검증
        if not validator.os_kind_is_valid(data[C.OS_KIND]):
            return _resp.Resp(C.ResponseCode.FIELD_INVALID)

        #: 기준 이메일
        an_email = data.get(C.EMAIL, "")

        if validator.data_is_empty(an_email):
            return _resp.Resp(C.ResponseCode.KEY_INVALID)

        #: PSQL
        users = _md_user_psql.put_user_from_mobile(an_email, data)

        #: Redis
        resp = _md_user_redis.put_user(an_email, users)

        #: File Make
        os.system("touch {0}/login_{1}".format(TMP_DOMAIN_PATH, an_email))

        #: Logger
        log_maker.logging_users(
            msg = "[NV] USER LOGIN", 
            email = an_email, 
            os = data.get(C.OS_KIND, C.UNKNOWN), 
            uuid = data.get(C.UUID, C.UNKNOWN),
            host = data.get(C.HOST, C.UNKNOWN)
        )

        return resp

    def receive_mobile_user_setting(self, data):
        """ 사용자 기기별 개별 설정(네이티브 기기 전용)"""
        if validator.data_is_empty(data):
            return _resp.Resp(C.ResponseCode.NO_DATA)

        if not validator.setting_data_is_valid(data):
            return _resp.Resp(C.ResponseCode.DATA_INSUFFICIENT)

        resp = {}

        #: 기존 설정정보
        nu_email = data[C.EMAIL]
        nu_uuid = "{0}{1}".format(data[C.UUID], C.NATIVE_POSTFIX)
        prefs = _md_user_psql.get_users_by_uuid(nu_email, nu_uuid)

        #: 사용자 등록되어있지 않을경우
        if validator.data_is_empty(prefs):
            return _resp.Resp(C.ResponseCode.NO_USER_REGISTERED)

        settings = {
            C.AN_EMAIL : data[C.EMAIL],
            C.AN_UUID : "{0}{1}".format(data[C.UUID], C.NATIVE_POSTFIX),
            C.HOST : prefs[C.HOST],
            C.AU_ALL : data[C.NOTIFY_ALL]
        }

        try:
            #: 방해시간 (결과조건 : 리스트 사이즈 '2'가 아닌 경우)
            settings[C.AU_TIME] = prefs[C.AU_TIME]
            if C.DO_NOT_DISTURB_TIME in data:
                time_list = data[C.DO_NOT_DISTURB_TIME]
                if len(time_list) == 1 or len(time_list) > 2:
                    return _resp.Resp(C.ResponseCode.FIELD_INVALID)

                settings[C.AU_TIME] = utils.check_none_value(time_list, prefs[C.AU_TIME])

            #: 예외 메일함
            settings[C.AU_MAIL] = utils.check_none_value(data[C.EXCLUDE_MAIL], prefs[C.AU_MAIL])\
                if C.EXCLUDE_MAIL in data else prefs[C.AU_MAIL]

            #: 예외 전자결재 유형
            settings[C.AU_EAS] = utils.check_none_value(data[C.EXCLUDE_EAS], prefs[C.AU_EAS])\
                if C.EXCLUDE_EAS in data else prefs[C.AU_EAS]

            #: 예외 게시판 및 댓,답글 설정 
            settings[C.AU_BOARD] = prefs[C.AU_BOARD]
            if C.BOARD in data:
                if not C.EXCLUDE_FOLDERS in data[C.BOARD]:
                    return _resp.Resp(C.ResponseCode.FIELD_INVALID)
                if not C.NOTIFY_TO_ME in data[C.BOARD]:
                    return _resp.Resp(C.ResponseCode.FIELD_INVALID)

                settings[C.AU_BOARD] = utils.check_none_value(data[C.BOARD], prefs[C.AU_BOARD])

            #: 예외 캘린더
            settings[C.AU_CAL] = utils.check_none_value(data[C.EXCLUDE_CAL], prefs[C.AU_CAL])\
                if C.EXCLUDE_CAL in data else prefs[C.AU_CAL]

            #: PSQL
            users = _md_user_psql.put_user_setting_from_mobile(settings)

            #: Redis
            redis_result = _md_user_redis.put_user(data[C.EMAIL], users)

            if redis_result[C.RESULT]:
                resp = _resp.RespWithData(
                    C.ResponseCode.SUCCESS, 
                    self.make_setting_resp(settings)
                )
            else:
                resp = redis_result
        except Exception as e:
            resp = _resp.Resp(C.ResponseCode.USER_DB_HANDLING_ERROR)
            raise UserReceiveHandlerException(str(e))

        return resp

    def receive_mobile_user_logout(self, data):
        """ 사용자 로그아웃(네이티브 기기 전용)"""
        if validator.data_is_empty(data):
            return _resp.Resp(C.ResponseCode.NO_DATA)

        if not validator.logout_data_is_valid(data):
            return _resp.Resp(C.ResponseCode.DATA_INSUFFICIENT)

        del_data = {
            C.AN_EMAIL : data[C.EMAIL],
            C.AN_UUID : "{0}{1}".format(data[C.UUID], C.NATIVE_POSTFIX),
            C.AN_TYPE : data[C.OS_KIND]
        }

        return self.receive_remove_user(del_data)
        
    """
    사용자 IN / OUT 처리
    * 구 하이브리드 기기
    """
    def receive_put_user(self, data, ip):
        """ 사용자 로그인"""
        data = ast.literal_eval(json.dumps(data))
        if validator.data_instance(data, dict):
            tmpList = []
            tmpList.append(data)
            data = tmpList

        if data:
            an_email = data[0][C.AN_EMAIL]

            #: Logger
            log_maker.logging_users(
                msg = "[HB] USER_LOGIN",
                ip = ip, 
                email = an_email, 
                data = data
            )

            #: PSQL
            result = _md_user_psql.put_user(data)

            #: Redis
            _md_user_redis.put_user(an_email, result, data)

            #: File Make
            os.system("touch {0}/login_{1}".format(TMP_DOMAIN_PATH, an_email))

    def receive_notify_for_logout(self, data):
        """ 사용자 로그아웃 알림
        - 알림만 발송하며, 데이터 삭제는 없음
        """
        if validator.data_instance(data, list):
            data = data[0]

        an_email = data.get(C.AN_EMAIL, "")
        nu_uuid = data.get(C.AN_UUID, "")

        if validator.data_is_empty(an_email):
            return False

        try:
            #: PSQL
            result = _md_user_psql.get_dbs(an_email)

            #: '비밀번호 변경' 알림 
            if result:
                noti_launcher.logout(result, an_email, nu_uuid)

            pass

        except Exception as e:
            raise UserReceiveHandlerException(str(e))

    def receive_remove_user(self, data):
        """ 사용자 삭제(모바일기기 로그아웃)"""
        if validator.data_instance(data, list):
            data = data[0]

        result = False

        an_email = data.get(C.AN_EMAIL, "")
        an_uuid = data.get(C.AN_UUID, "")

        if validator.string_is_empty(an_email, an_uuid):
            return False

        try:
            #: Logger
            log_maker.logging_users(msg = "USER_LOGOUT", email = an_email, uuid = an_uuid)

            #: PSQL
            users = _md_user_psql.del_dbs(data, False)

            #: Redis                
            result = _md_user_redis.del_user(an_email, users)

            #: File Make
            os.system("touch {0}/logout_{1}".format(TMP_DOMAIN_PATH, an_email))
        except Exception as e:
            raise UserReceiveHandlerException(str(e))
        finally:
            return result

    def receive_remove_all_users(self, data):
        """ 사용자 전체삭제(비밀번호 변경과 같은 강제 로그아웃 작업)"""
        if validator.data_instance(data, list):
            data = data[0]

        an_email = data.get(C.AN_EMAIL, "")

        if validator.data_is_empty(an_email):
            return False

        try:
            #: Logger
            log_maker.logging_users(msg = "USER_ALL_LOGOUT", email = an_email)

            #: PSQL            
            result = _md_user_psql.del_dbs(data, True)

            #: Redis 
            _md_user_redis.del_user(an_email, result)

            #: File Make
            os.system("touch {0}/logout_{1}".format(TMP_DOMAIN_PATH, an_email))
        except Exception as e:
            raise UserReceiveHandlerException(str(e))

    def receive_language(self, data):
        """ 사용자 언어변경"""
        nu_uuid = data.get(C.NU_UUID, "")

        if validator.data_is_empty(nu_uuid):
            return False

        #: PSQL
        result = _md_user_psql.set_language(data)

        #: Redis
        if result:
            nu_email = result[0][C.NU_EMAIL]
            _md_user_redis.put_user(nu_email, result)

    def make_setting_resp(self, _s):
        """ 설정 작업 후, 데이터 Resp 재정리"""
        if validator.data_is_empty(_s):
            return {}

        return {
            C.EMAIL : _s[C.AN_EMAIL],
            C.UUID : _s[C.AN_UUID].replace(C.NATIVE_POSTFIX, ""),
            C.NOTIFY_ALL : {
                C.MAIL : _s[C.AU_ALL][C.MAIL], 
                C.EAS : _s[C.AU_ALL][C.EAS], 
                C.BOARD : _s[C.AU_ALL][C.BOARD], 
                C.CAL : _s[C.AU_ALL][C.CAL]
            },
            C.DO_NOT_DISTURB_TIME : _s[C.AU_TIME],
            C.EXCLUDE_MAIL : _s[C.AU_MAIL],
            C.EXCLUDE_EAS : _s[C.AU_EAS],
            C.EXCLUDE_CAL : _s[C.AU_CAL],
            C.BOARD : {
                C.EXCLUDE_FOLDERS : _s[C.AU_BOARD][C.EXCLUDE_FOLDERS],
                C.NOTIFY_TO_ME : {
                    C.COMMENT : _s[C.AU_BOARD][C.NOTIFY_TO_ME][C.COMMENT],
                    C.REPLY : _s[C.AU_BOARD][C.NOTIFY_TO_ME][C.REPLY]
                }
            },
        }


if __name__ == "__main__":
    urh = UserReceiveHandler()  
