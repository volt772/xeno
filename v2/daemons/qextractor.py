#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
import time
from multiprocessing import Process, cpu_count

from v2 import const as C
from v2.daemons import daemon_logger
from v2.handlers.sender.sd_dispatch import SendDispatcher

""" 큐 실행기
Redis에 저장된 모든 알림큐를 순차적으로 꺼낸 후,
발송할 수 있도록 발송기에 전달
"""

_dispatcher = SendDispatcher()


def run():
    while True:
        try:
            _dispatcher.send_notification()
            time.sleep(float(1.0))
        except Exception as e:
            daemon_logger.save_log(
                C.Logger.QEXTRACTOR,
                "{0} [RunErr : {1}]".format(datetime.datetime.now(), str(e)),
            )


if __name__ == "__main__":
    startTime = time.time()

    num_cores = cpu_count() - 2

    #: 개발 서버 등, core 음수일경우 == 1
    if num_cores < 0:
        num_cores = 1

    # Create num_cores sub-processes to do the work
    processes = []
    for i in range(num_cores):
        processes.append(Process(target=run, args=()))

    for i in range(num_cores):
        processes[i].start()

    for i in range(num_cores):
        processes[i].join()

    endTime = time.time()
    workTime = endTime - startTime
