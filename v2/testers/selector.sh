#!/bin/bash

echo '
██╗  ██╗███████╗███╗   ██╗ ██████╗     ████████╗███████╗███████╗████████╗███████╗██████╗
╚██╗██╔╝██╔════╝████╗  ██║██╔═══██╗    ╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██╔════╝██╔══██╗
 ╚███╔╝ █████╗  ██╔██╗ ██║██║   ██║       ██║   █████╗  ███████╗   ██║   █████╗  ██████╔╝
 ██╔██╗ ██╔══╝  ██║╚██╗██║██║   ██║       ██║   ██╔══╝  ╚════██║   ██║   ██╔══╝  ██╔══██╗
██╔╝ ██╗███████╗██║ ╚████║╚██████╔╝       ██║   ███████╗███████║   ██║   ███████╗██║  ██║
╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝        ╚═╝   ╚══════╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝'



read -p "---------------------------------- [테스트 선택] ----------------------------------

#################################### [100 iOS 하이브리드 테스트] ###########################
[101] iOS 하이브리드 로그인
[102] iOS 하이브리드 로그아웃
[103] iOS 하이브리드 기기 언어변경
[104] iOS 하이브리드 로그아웃 알림

#################################### [120 네이티브 테스트] ##################################
[121] 네이티브 로그인 (라우팅 : /mo_login)
[122] 네이티브 로그아웃 (라우팅 : /mo_logout)
[123] 사용자 전부삭제(메신저와 웹훅을 제외한 모두)
[124] 네이티브 설정 (라우팅 : /mo_setting)
[125] TASK 로그인 (라우팅 : /mo_login)
[126] TASK 로그아웃 (라우팅 : /mo_logout)
[127] 게시판 알림 데이터 수신
[128] 전자결재 알림 데이터 수신
[129] TASK 알림 데이터 수신

#################################### [140 메신저 테스트] #####################################
[141] 사용자 커넥션 등록
[142] 사용자 커넥션 해제
[143] 메신저 TASK 로그인
[144] 메신저 TASK 로그아웃

#################################### [160 웹훅 테스트] #######################################
[161] 사용자 웹훅 등록
[162] 사용자 웹훅 삭제

################################### [200 큐 데이터 테스트] ###################################

[201] : 메일 데이터 밀어넣기 [notifier 데몬 선행]
[202] : 메일 외 데이터 밀어넣기 [notifier 데몬 선행]
[203] : 메일 데이터 삽입 시, 특수고객 조건검사
[204] : 큐 발송 [전체기기]
[205] : 캘린더 알림 발송 [전체기기]

#################################### [300 도메인 테스트] #####################################

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

################################### [600 EXTRAS 데이터 테스트] ##############################


################################### [700 공석] ##############################################

################################### [800 CalDAV 데이터 테스트] ##############################

[801] :  CalDAV 큐 추가(캘린더생성)
[802] :  CalDAV 큐 추가(캘린더삭제)
[803] :  CalDAV 큐 추가(일정등록)
[804] :  CalDAV 큐 추가(일정수정)
[805] :  CalDAV 큐 추가(일정삭제)

################################### [900 커스텀 명령 테스트] ###################################

[901] : 강제 로그아웃 

`echo $'\n> '`" test_num

cd /root/workspace/src/app-notify/v2/testers/

if [ "${test_num}" -eq 101 ]; then
	/root/workspace/xeno/bin/python -m unittest users.te_hybrid.UserTester.test_login_ios_hybrid
elif [ "${test_num}" -eq 102 ]; then
	/root/workspace/xeno/bin/python -m unittest users.te_hybrid.UserTester.test_logout_ios_hybrid
elif [ "${test_num}" -eq 103 ]; then
	/root/workspace/xeno/bin/python -m unittest users.te_hybrid.UserTester.test_ios_hybrid_language
elif [ "${test_num}" -eq 104 ]; then
	/root/workspace/xeno/bin/python -m unittest users.te_hybrid.UserTester.test_ios_hybrid_logout_notification

elif [ "${test_num}" -eq 121 ]; then
	/root/workspace/xeno/bin/python -m unittest users.te_native.UserTester.test_login_mobile
elif [ "${test_num}" -eq 122 ]; then
	/root/workspace/xeno/bin/python -m unittest users.te_native.UserTester.test_logout_mobile
elif [ "${test_num}" -eq 123 ]; then
	/root/workspace/xeno/bin/python -m unittest users.te_native.UserTester.test_logout_all_users
elif [ "${test_num}" -eq 124 ]; then
	/root/workspace/xeno/bin/python -m unittest users.te_native.UserTester.test_setting_mobile
elif [ "${test_num}" -eq 125 ]; then
	/root/workspace/xeno/bin/python -m unittest users.te_native.UserTester.test_login_task_mobile
elif [ "${test_num}" -eq 126 ]; then
	/root/workspace/xeno/bin/python -m unittest users.te_native.UserTester.test_logout_task_mobile
elif [ "${test_num}" -eq 127 ]; then
	/root/workspace/xeno/bin/python -m unittest users.te_native.UserTester.test_insert_board_queue
elif [ "${test_num}" -eq 128 ]; then
	/root/workspace/xeno/bin/python -m unittest users.te_native.UserTester.test_insert_eas_queue
elif [ "${test_num}" -eq 129 ]; then
	/root/workspace/xeno/bin/python -m unittest users.te_native.UserTester.test_insert_task_queue

elif [ "${test_num}" -eq 141 ]; then
	/root/workspace/xeno/bin/python -m unittest users.te_messenger.UserTester.test_login_messenger_connection
elif [ "${test_num}" -eq 142 ]; then
	/root/workspace/xeno/bin/python -m unittest users.te_messenger.UserTester.test_logout_messenger_connection
elif [ "${test_num}" -eq 143 ]; then
	/root/workspace/xeno/bin/python -m unittest users.te_messenger.UserTester.test_login_task_messenger
elif [ "${test_num}" -eq 144 ]; then
	/root/workspace/xeno/bin/python -m unittest users.te_messenger.UserTester.test_logout_task_messenger

elif [ "${test_num}" -eq 161 ]; then
	/root/workspace/xeno/bin/python -m unittest users.te_webhook.UserTester.test_apply_user_webhook
elif [ "${test_num}" -eq 162 ]; then
	/root/workspace/xeno/bin/python -m unittest users.te_webhook.UserTester.test_del_user_webhook

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
elif [ "${test_num}" -eq 901 ]; then
	/root/workspace/xeno/bin/python -m unittest te_prompt.PromptTester.test_prompt_logout
else
	echo "---------------------------------- [알수없는 테스트] ----------------------------------"
fi
