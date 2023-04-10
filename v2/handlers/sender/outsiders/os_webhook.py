#!/usr/bin/python3
# -*- coding: utf-8 -*-

import base64
import datetime
import os
import re
import time
import urllib

from v2 import const as C
from v2.handlers.sender.sd_utils import SendUtilHandler
from v2.helpers import log_maker, utils, validator
from v2.models import _md_mail


""" 웹훅 알림 발송
큐에 저장된 메일 관련 알림을 조건 검사후, 등록된 웹훅 API에 발송한다
"""

_send_utils = SendUtilHandler()


class WebHookHandlerException(Exception):
    def __init__(self, msg=""):
        self.msg = msg
        log_maker.logging_default(
            log_type=C.Logger.OS_WEBHOOK, msg=str(msg), sentry=False
        )

    def __str__(self):
        return self.msg


class WebHookHandler:
    def __init__(self):
        pass

    def send_webhook(self, data, device):
        """Webhook 수신"""
        if validator.data_is_empty(data) and validator.data_is_empty(device):
            return False

        try:
            b64url = device["au_hook_curl"]
            curl_url = base64.b64decode(b64url).decode("utf-8")
        except Exception as e:
            raise WebHookHandlerException(str(e))

        try:
            for _type, _rep in C.WebhookData.INDICATOR.items():
                replace_string = ""
                if _type != "count":
                    replace_string = data[_type]

                    #: [치환] 타입
                    if _type == "type":
                        replace_string = C.WebhookData.TYPES[data[_type]]

                    elif _type == "subject":
                        _subject = (
                            data[_type].replace("'", "'\\'''").replace("\\u", "\\\\u")
                        )
                        replace_string = utils.get_surrogatepass_str(_subject)

                    #: [치환] 연결주소
                    elif _type == "ref_url":
                        _host = _md_mail.get_webmail_info(
                            device.get("an_email"), "WEBMAIL_HOST"
                        )
                        redirect_url = "https://{0}{1}".format(
                            _host, urllib.parse.unquote(data["ref_url"])
                        )
                        replace_string = redirect_url

                elif _type == "count":
                    email = data["to"]

                    replace_string = str(
                        _send_utils.get_unread_count(email, True, None)
                    )

                curl_url = curl_url.replace(_rep, replace_string)

            if "{__DATE:" in curl_url:
                curl_url = self.make_custom_date(curl_url, data["date"])

            self.do_send(self.replace_quota(curl_url))
        except Exception as e:
            raise WebHookHandlerException(str(e))

    def make_custom_date(self, _url, _date):
        """날짜형식(사용자커스텀)"""
        try:
            orig_format = re.search(r"\{__(.*?)__\}", _url).group(1)
            date_format = self.format_recheck(orig_format)

            if date_format:
                user_format = date_format.replace("DATE:", "")
                timestamp = int(
                    time.mktime(
                        datetime.datetime.strptime(
                            _date, "%Y-%m-%d %H:%M:%S"
                        ).timetuple()
                    )
                )
                formd_date = time.strftime(user_format, time.localtime(timestamp))

                url = _url.replace("{__%s__}" % (orig_format), formd_date)

                return url
        except Exception:
            return _url

    def format_recheck(self, _format):
        """날짜형식검사 및 치환"""
        _format = _format.replace("%D", "%d")
        _format = _format.replace("%h", "%H")
        _format = _format.replace("%s", "%S")

        return _format

    def replace_quota(self, curl_url):
        """Quota 기호 치환"""
        curl_url = curl_url.replace("''", "'").replace('\\"', '"').replace("'", "'")

        return curl_url

    def do_send(self, curl_url):
        """API 발송 및 로깅"""
        try:
            result_code = os.system(curl_url)
            logMsg = "[code : %d] - [WEBHOOK] %s " % (result_code, curl_url)
            log_maker.logging_webhook(logMsg)
        except Exception as e:
            raise WebHookHandlerException(str(e))


if __name__ == "__main__":
    whh = WebHookHandler()
