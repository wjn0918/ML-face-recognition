"""服务端"""


import os

import hprose
from apscheduler.schedulers.background import BackgroundScheduler

from master import action, init


def faceRecognition(image):
    """
    预测文本类别
    :param doc: 需要分类的文本
    :return:
    """
    r = action(image)
    return r


def main():
    scheduler = BackgroundScheduler()
    # 间隔3秒钟执行一次
    # scheduler.add_job(init, 'interval', seconds=3)
    # 定时任务12:00执行
    scheduler.add_job(init, 'cron', hour=24, minute=0)
    # 这里的调度任务是独立的一个线程
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        # 主任务是独立的线程执行
        server = hprose.HttpServer(port=8181)
        server.addFunction(faceRecognition)
        server.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print('Exit The Job!')



if __name__ == '__main__':
    main()
