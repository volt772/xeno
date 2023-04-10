#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging
import os

from v2 import const as _cv

""" 로깅시스템
프로그램 전반에 걸친 모든 로그 생성 및 관리하며,
상황별, 데몬별 구분하여 로그파일을 관리한다.
"""

_BASIC_PATH = _cv.LocalPath.LOG_DAEMONS
_LOGGER = {
    _cv.Logger.DEXTRACTOR: None,
    _cv.Logger.QEXTRACTOR: None,
    _cv.Logger.DEFAULT: None,
}

formatter = logging.Formatter("%(asctime)s [%(message)s]")


def setup_logger(name, log_file, level=logging.INFO):
    """로그 기본설정"""
    log_path = "{0}/{1}".format(_BASIC_PATH, log_file)

    mode = "a"
    handler = logging.FileHandler(log_path, mode=mode, encoding="utf8")
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.propagate = False

    return logger


def save_log(kind, msg):
    """로그 저장"""
    if not kind or not msg:
        return False

    log_name = kind
    log_file = _cv.Logger.FILE[kind]

    _log = None
    if not _LOGGER[kind]:
        _log = setup_logger(log_name, log_file)
        _LOGGER[kind] = _log
    else:
        try:
            log_full_path = "{0}/{1}".format(_BASIC_PATH, log_file)
            if not os.path.exists(log_full_path):
                _log = setup_logger(log_name, log_file)
            else:
                _log = _LOGGER[kind]
        except Exception:
            pass

    try:
        _log.info(msg)
    except Exception:
        pass


if __name__ == "__main__":
    pass
