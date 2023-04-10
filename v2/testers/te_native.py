#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import random
import time
import unittest

from v2.handlers.receiver import _board, _eas, _user, _veryhub

""" UserTester
- Tester 사용자
"""


class UserTester(unittest.TestCase):

    ip = "1.1.1.1"

    start_time = 0
    end_time = 0

    with open("./datum.json") as json_file:
        json_data = json.load(json_file)

    def setUp(self):
        self.__class__.start_time = time.time()

    def tearDown(self):
        self.__class__.end_time = time.time() - self.__class__.start_time
        print(" >>>>>>>>>>> Elapsed Seconds : {0}".format(self.__class__.end_time))

    """
    Native Devices
    """

    def test_login_mobile(self):
        """[121] 네이티브 로그인 (라우팅 : /mo_login)"""
        print(
            """
        ===========================================================================================
            [121] 네이티브 로그인 (라우팅 : /mo_login)
            * 네이티브 기기로 로그인한다
            * 신규 라우팅 /mo_login으로 로그인한다.
        ===========================================================================================
        """
        )

        data = self.__class__.json_data["login_android_native"]
        # data = self.__class__.json_data["login_ios_native"]
        result = _user.receive_mobile_user_login(data)
        print("[R] : ", result)

    def test_logout_mobile(self):
        """[122] 네이티브 로그아웃 (라우팅 : /mo_logout)"""
        print(
            """
        ===========================================================================================
            [122] 네이티브 로그아웃 (라우팅 : /mo_logout)
            * 네이티브 기기를 로그아웃한다
            * 신규 라우팅 /mo_logout으로 로그아웃한다.
        ===========================================================================================
        """
        )
        # data = self.__class__.json_data["logout_android_native"]
        data = self.__class__.json_data["logout_ios_native"]
        result = _user.receive_mobile_user_logout(data)
        print("[R] : ", result)

    def test_logout_all_users(self):
        """[123] 사용자 전부삭제(메신저와 웹훅을 제외한 모두)"""
        print(
            """
        ===========================================================================================
            [123] 사용자 전부삭제(메신저와 웹훅을 제외한 모두)
            * 메신저와 웹훅을 제외한 모두 삭제한다.
        ===========================================================================================
        """
        )
        data = self.__class__.json_data["delete_all_user_execept_messenger_webhook"]
        result = _user.receive_remove_all_users(data)
        print("[R] : ", result)

    def test_setting_mobile(self):
        """[124] 네이티브 설정 (라우팅 : /mo_setting)"""
        print(
            """
        ===========================================================================================
            [124] 네이티브 설정 (라우팅 : /mo_setting)
            * 네이티브 기기의 설정정보를 저장한다
        ===========================================================================================
        """
        )
        data = self.__class__.json_data["settings_native"]
        result = _user.receive_mobile_user_setting(data)
        print("[R] : ", result)

    def test_login_task_mobile(self):
        """[125] TASK 로그인 (라우팅 : /mo_login)"""
        print(
            """
        ===========================================================================================
            [125] TASK 로그인 (라우팅 : /mo_login)
            * TASK앱에서 로그인한다.
            * 통합 라우팅 /mo_login으로 로그인한다.
        ===========================================================================================
        """
        )

        data = self.__class__.json_data["login_task_native"]
        result = _user.receive_mobile_user_login(data)
        print("[R] : ", result)

    def test_logout_task_mobile(self):
        """[126] TASK 로그아웃 (라우팅 : /mo_logout)"""
        print(
            """
        ===========================================================================================
            [126] TASK 로그아웃 (라우팅 : /mo_logout)
            * TASK앱에서 로그아웃한다.
            * 통합 라우팅 /mo_logout으로 로그아웃한다.
        ===========================================================================================
        """
        )
        data = self.__class__.json_data["logout_task_native"]
        result = _user.receive_mobile_user_logout(data)
        print("[R] : ", result)

    def test_insert_board_queue(self):
        """[127] 게시판 알림 데이터 수신"""
        print(
            """
        ===========================================================================================
            [127] 게시판 알림 데이터 수신
            * 게시판 알림 대상 데이터를 Redis 큐에 삽입한다.
        ===========================================================================================
        """
        )
        data = self.__class__.json_data["queue_board"]
        result = _board.receive_board(data)
        print("[R] : ", result)

    def test_insert_eas_queue(self):
        """[128] 전자결재 알림 데이터 수신"""
        print(
            """
        ===========================================================================================
            [128] 전자결재 알림 데이터 수신
            * 전자결재 알림 대상 데이터를 Redis 큐에 삽입한다.
        ===========================================================================================
        """
        )
        data = self.__class__.json_data["queue_eas"]
        result = _eas.receive_eas(data)
        print("[R] : ", result)

    def test_insert_task_queue(self):
        """[129] TASK 알림 데이터 수신"""
        print(
            """
        ===========================================================================================
            [129] TASK 알림 데이터 수신
            * TASK 알림 대상 데이터를 Redis 큐에 삽입한다.
        ===========================================================================================
        """
        )
        noti_types = {
            "cardDeleted": ["실행자", "카드명"],
            "comment": ["실행자", "카드명"],
            "cardDescUpdated": ["실행자", "카드명"],
            "cardUnsubscribed": ["실행자", "카드명"],
            "cardSubscribed": ["실행자", "카드명"],
            "cardNameUpdated": ["실행자", "카드명"],
            "cardCreated": ["실행자", "섹션이름", "카드명"],
            "cardAttachDeleted": ["실행자", "카드명", "파일명"],
            "cardAttachCreated": ["실행자", "카드명", "파일명"],
            "cardAssigneeAdded": ["실행자", "카드명", "담당자명"],
            "cardAssigneeRemoved": ["실행자", "카드명", "담당자명"],
            "cardChecklistAdded": ["실행자", "카드명", "체크리스트 이름"],
            "cardChecklistCompleted": ["실행자", "카드명", "체크리스트 이름"],
            "cardChecklistIncomplete": ["실행자", "카드명", "체크리스트 이름"],
            "cardChecklistRemoved": ["실행자", "카드명", "체크리스트 이름"],
            "cardLabelAdded": ["실행자", "카드명", "라벨이름"],
            "cardLabelRemoved": ["실행자", "카드명", "라벨이름"],
            "cardStatusCompleted": ["실행자", "카드명", "완료"],
            "cardStatusIncomplete": ["실행자", "카드명", "미완료"],
            "cardDueUpdated": ["실행자", "카드명", "as-is기한", "to-be 기한"],
            "cardSectionMoved": ["실행자", "카드명", "as-is 섹션이름", "to-be 섹션이름"],
            "cardRequesterUpdated": ["실행자", "카드명", "as-is 요청자명", "to-be 요청자명"],
            "sectionDeleted": ["실행자", "섹션 이름"],
            "spaceDeleted": ["실행자", "공간 이름"],
        }

        for i in range(1):
            random_noti = random.choice(list(noti_types.items()))
            alaram_type = random_noti[0]
            alaram_data = random_noti[1]

            data = {
                "notiType": "task",
                # 'pushTargetEmailList': ['hnjeong@b53.myplug.kr', 'tjwogns@b53.myplug.kr'],
                # 'pushTargetEmailList': ['hnjeong@b53.myplug.kr'],
                "pushTargetEmailList": [],
                "messengerTargetEmailList": ["hnjeong@b53.myplug.kr"],
                # 'messengerTargetEmailList': [],
                "link": "https://task.wiro.kr/spaces/10/cards/11",
                "alarmType": alaram_type,
                "data": alaram_data,
                "ids": {
                    "spaceId": 5,
                    "boardId": 1,
                    "sectionId": 1,
                    "oldSectionId": 1,
                    "cardId": 1,
                    "commentId": 1335,
                },
            }

            result = _veryhub.veryhub_distributor(data)
            print("[R] : ", result)
