#!/bin/bash

echo '
██╗  ██╗███████╗███╗   ██╗ ██████╗     ████████╗███████╗███████╗████████╗███████╗██████╗
╚██╗██╔╝██╔════╝████╗  ██║██╔═══██╗    ╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██╔════╝██╔══██╗
 ╚███╔╝ █████╗  ██╔██╗ ██║██║   ██║       ██║   █████╗  ███████╗   ██║   █████╗  ██████╔╝
 ██╔██╗ ██╔══╝  ██║╚██╗██║██║   ██║       ██║   ██╔══╝  ╚════██║   ██║   ██╔══╝  ██╔══██╗
██╔╝ ██╗███████╗██║ ╚████║╚██████╔╝       ██║   ███████╗███████║   ██║   ███████╗██║  ██║
╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝        ╚═╝   ╚══════╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝'



read -p "---------------------------------- [테스트 선택] ----------------------------------

#################################### [100 사용자테스트] ####################################

[101] : 하이브리드 로그인
[102] : 네이티브 로그인(Aeolos1)
[103] : 네이티브 로그인(Aeolos2)
[104] : 사용자 웹훅 등록
[105] : 사용자 퍼들러 커넥션 등록 (hnjeong)
[106] : 사용자 기기 언어변경, 하이브리드
[107] : 하이브리드 로그아웃(강제, 비번변경시 등..)
[108] : 사용자 삭제(퍼들러와 웹훅을 제외한 모두)
[109] : 네이티브 로그아웃(Aeolos1) [102번 선행]
[110] : 사용자 삭제(하이브리드 로그아웃) [101번 선행]
[111] : 사용자 삭제(웹훅) [104번 선행]
[112] : 사용자 삭제(멀티 UUID 커스텀 삭제)
[113] : 사용자 멀티등록(멀티 UUID 커스텀 등록)
[114] : 네이티브 로그인 (라우팅 : /mo_login)
[115] : 네이티브 로그아웃 (라우팅 : /mo_logout)
[116] : 네이티브 설정 (라우팅 : /mo_setting)
[117] : 사용자 에러핸들링 Response 확인

################################### [200 큐 데이터 테스트] ###################################

[201] : 메일 데이터 밀어넣기 [notifier 데몬 선행]
[202] : 메일 외 데이터 밀어넣기 [notifier 데몬 선행]
[203] : 메일 데이터 삽입 시, 특수고객 조건검사
[204] : 큐 발송 [전체기기]
[205] : 캘린더 알림 발송 [전체기기]

#################################### [300 도메인 테스트] ####################################

[301] : 도메인정보 등록
[302] : 도메인정보 변경 
[303] : 도메인정보 삭제

#################################### [400 캘린더 테스트] ####################################

[401] : 캘린더 이벤트 추가
[402] : 캘린더 이벤트 삭제  

################################### [500 스케쥴러 테스트] ###################################

[501] : 크론탭, 캘린더 발송
[502] : 크론탭, 캘린더 지난 이벤트 삭제
[503] : 크론탭, 사용자 Redis 데이터 동기화

################################### [600 게시판 데이터 테스트] ###################################

[601] : 게시판 데이터 등록 

################################### [700 전자결재 데이터 테스트] ###################################

[701] : 전자결재 데이터 등록 

################################### [800 CalDAV 데이터 테스트] ###################################

[801] :  CalDAV 큐 추가(캘린더생성)
[802] :  CalDAV 큐 추가(캘린더삭제)
[803] :  CalDAV 큐 추가(일정등록)
[804] :  CalDAV 큐 추가(일정수정)
[805] :  CalDAV 큐 추가(일정삭제)

`echo $'\n> '`" test_num

cd /root/workspace/src/app-notify/v2/testers/

if [ "${test_num}" -eq 101 ]; then
	/root/workspace/xeno/bin/python -m unittest te_user.UserTester.test_login_hybrid
elif [ "${test_num}" -eq 102 ]; then
	/root/workspace/xeno/bin/python -m unittest te_user.UserTester.test_login_aeolos1
elif [ "${test_num}" -eq 103 ]; then
	/root/workspace/xeno/bin/python -m unittest te_user.UserTester.test_login_aeolos2
elif [ "${test_num}" -eq 104 ]; then
	/root/workspace/xeno/bin/python -m unittest te_user.UserTester.test_apply_user_webhook
elif [ "${test_num}" -eq 105 ]; then
	/root/workspace/xeno/bin/python -m unittest te_user.UserTester.test_apply_user_puddlr
elif [ "${test_num}" -eq 106 ]; then
	/root/workspace/xeno/bin/python -m unittest te_user.UserTester.test_language
elif [ "${test_num}" -eq 107 ]; then
	/root/workspace/xeno/bin/python -m unittest te_user.UserTester.test_logout_hybrid
elif [ "${test_num}" -eq 108 ]; then
	/root/workspace/xeno/bin/python -m unittest te_user.UserTester.test_del_users_all
elif [ "${test_num}" -eq 109 ]; then
	/root/workspace/xeno/bin/python -m unittest te_user.UserTester.test_logout_aeolos1
elif [ "${test_num}" -eq 110 ]; then
	/root/workspace/xeno/bin/python -m unittest te_user.UserTester.test_del_user_mobile
elif [ "${test_num}" -eq 111 ]; then
	/root/workspace/xeno/bin/python -m unittest te_user.UserTester.test_del_user_webhook
elif [ "${test_num}" -eq 112 ]; then
	/root/workspace/xeno/bin/python -m unittest te_user.UserTester.test_del_users_by_multiple_uuids
elif [ "${test_num}" -eq 113 ]; then
	/root/workspace/xeno/bin/python -m unittest te_user.UserTester.test_login_all_uuids
elif [ "${test_num}" -eq 114 ]; then
	/root/workspace/xeno/bin/python -m unittest te_user.UserTester.test_login_mo_login
elif [ "${test_num}" -eq 115 ]; then
	/root/workspace/xeno/bin/python -m unittest te_user.UserTester.test_logout_mo_logout
elif [ "${test_num}" -eq 116 ]; then
	/root/workspace/xeno/bin/python -m unittest te_user.UserTester.test_noti_setting_mo_setting
elif [ "${test_num}" -eq 117 ]; then
	/root/workspace/xeno/bin/python -m unittest te_user.UserTester.test_reponse_errors
elif [ "${test_num}" -eq 201 ]; then
	file="/root/workspace/src/domain_list/fcm_dom_list/hnjeong@b53.myplug.kr"
	if [ ! -f "$file" ]
	then
		touch $file
	fi
	/usr/bin/python /root/workspace/src/app-notify/v2/testers/queue_maker.py
elif [ "${test_num}" -eq 202 ]; then
	file="/root/workspace/src/domain_list/fcm_dom_list/hnjeong@b53.myplug.kr"
	if [ ! -f "$file" ]
	then
		touch $file
	fi
	/usr/bin/python /root/workspace/src/app-notify/v2/testers/queue_ext_maker.py
elif [ "${test_num}" -eq 203 ]; then
	/root/workspace/xeno/bin/python -m unittest te_dispatch.DispatchTester.test_insert_check_exceptional_custom
elif [ "${test_num}" -eq 204 ]; then
	/root/workspace/xeno/bin/python -m unittest te_dispatch.DispatchTester.test_dispatch_mail
elif [ "${test_num}" -eq 205 ]; then
	/root/workspace/xeno/bin/python -m unittest te_dispatch.DispatchTester.test_dispatch_calendar
elif [ "${test_num}" -eq 301 ]; then
	/root/workspace/xeno/bin/python -m unittest te_domain.DomainTester.test_apply_domain_info
elif [ "${test_num}" -eq 302 ]; then
	/root/workspace/xeno/bin/python -m unittest te_domain.DomainTester.test_change_domain_info
elif [ "${test_num}" -eq 303 ]; then
	/root/workspace/xeno/bin/python -m unittest te_domain.DomainTester.test_delete_domain_info
elif [ "${test_num}" -eq 401 ]; then
	/root/workspace/xeno/bin/python -m unittest te_calendar.CalendarTester.test_add_calendar
elif [ "${test_num}" -eq 402 ]; then
	/root/workspace/xeno/bin/python -m unittest te_calendar.CalendarTester.test_del_calendar
elif [ "${test_num}" -eq 501 ]; then
	/root/workspace/xeno/bin/python -m unittest te_scheduler.SchedulerTester.test_crontab_calendar_send
elif [ "${test_num}" -eq 502 ]; then
	/root/workspace/xeno/bin/python -m unittest te_scheduler.SchedulerTester.test_crontab_calendar_delete
elif [ "${test_num}" -eq 503 ]; then
	/root/workspace/xeno/bin/python -m unittest te_scheduler.SchedulerTester.test_crontab_user_sync
elif [ "${test_num}" -eq 601 ]; then
	/root/workspace/xeno/bin/python -m unittest te_board.BoardTester.test_insert_board
elif [ "${test_num}" -eq 701 ]; then
	/root/workspace/xeno/bin/python -m unittest te_eas.EasTester.test_insert_eas
elif [ "${test_num}" -eq 801 ]; then
	/root/workspace/xeno/bin/python -m unittest te_caldav.CalDavTester.test_create_calendar
elif [ "${test_num}" -eq 802 ]; then
	/root/workspace/xeno/bin/python -m unittest te_caldav.CalDavTester.test_delete_calendar
elif [ "${test_num}" -eq 803 ]; then
	/root/workspace/xeno/bin/python -m unittest te_caldav.CalDavTester.test_create_event
elif [ "${test_num}" -eq 804 ]; then
	/root/workspace/xeno/bin/python -m unittest te_caldav.CalDavTester.test_modify_event
elif [ "${test_num}" -eq 805 ]; then
	/root/workspace/xeno/bin/python -m unittest te_caldav.CalDavTester.test_delete_event
else
	echo "---------------------------------- [알수없는 테스트] ----------------------------------"
fi
