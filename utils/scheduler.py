from apscheduler.schedulers.background import BackgroundScheduler
from utils.faceStore import faceStore
import os

def faceStoreScheduler():
    scheduler = BackgroundScheduler()
    # 间隔3秒钟执行一次
    # scheduler.add_job(faceStore, 'interval', seconds=3)
    # 定时任务12:00执行
    scheduler.add_job(faceStore, 'cron', hour=24, minute=0)
    # 这里的调度任务是独立的一个线程
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))



