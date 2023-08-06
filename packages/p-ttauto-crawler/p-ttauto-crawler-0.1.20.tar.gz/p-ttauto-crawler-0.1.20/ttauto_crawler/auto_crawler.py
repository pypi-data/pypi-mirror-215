import sys
import os
import time
from ttauto_crawler import utils
from ttauto_crawler import txt2proj
from ttauto_crawler import downloader
from ttauto_crawler import video_random_cutter
from ttauto_crawler import processing
from ttauto_crawler import uploading
from ttauto_crawler import task
from template_generator import binary as genertor_binary
from threading import Thread, current_thread, Lock
import calendar
from urllib.parse import *
import queue
import requests
import json
import random
import socket

THEADING_LIST = []
lock = Lock()

def qyWechatRobot(param):
    try:
        s = requests.session()
        s.headers.update({'Connection':'close'})
        headers = dict()
        headers['Content-Type'] = "application/json"
        res = s.post(f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ab1e9959-5bb2-4c7f-aa85-221bccffcea8", json.dumps(param), headers=headers, verify=False)
        print(res.content)
        s.close()
    except Exception as e:
        utils.logInfo(f"===== qyapi.weixin.qq.com fail ")

class CralwerStateThread(Thread):
    running = False
    machine_name = socket.gethostname()
    last_data = None
    def __init__(self):
        super().__init__()
        self.running = True
        self.daemon = True
        self.start()
    def run(self):
        qyWechatRobot({
            "msgtype": "text",
            "text": {
                "content": f"爬虫机<{self.machine_name}> 上线"
            }
        })
        while self.running:
            time.sleep(60)
            try:
                data = task.allTaskState(lock)
                if len(data["task_list"].strip()) == 0:
                    param = {
                        "msgtype": "text",
                        "text": {
                            "content": f"爬虫机<{self.machine_name}> 空载"
                        }
                    }
                    qyWechatRobot(param)
                else:
                    if (self.last_data != None and data != None and 
                                data["task_list"] == self.last_data["task_list"] and 
                                data["downloading"] == self.last_data["downloading"] and 
                                data["processing"] == self.last_data["processing"] and 
                                data["uploading"] == self.last_data["uploading"]):
                        continue
                    self.last_data = data
                    task_list = data["task_list"]
                    downloading = data["downloading"]
                    processing = data["processing"]
                    uploading = data["uploading"]
                    param = {
                        "msgtype": "markdown",
                        "markdown": {
                            "content": f"爬虫机<<font color=\"warning\">{self.machine_name}</font>> 目前处理任务：{task_list} \n\
                                >下载<font color=\"warning\">{downloading}</font> \n\
                                >合成<font color=\"warning\">{processing}</font> \n\
                                >上传<font color=\"warning\">{uploading}</font>"
                        }
                    }
                    qyWechatRobot(param)
            except:
                utils.logInfo(f"===== somthing CralwerStateThread fail")
    def markStop(self):
        self.running = False

class CralwerThread(Thread):
    running = False
    type = task.C_STATE.WAIT_DOWNLOAD
    def __init__(self, t=task.C_STATE.WAIT_DOWNLOAD):
        super().__init__()
        self.running = True
        self.daemon = True
        self.type = t
        self.start()
    def run(self):
        while self.running:
            if self.type == task.C_STATE.DOWNLOADING:
                taskItem = task.popDownload(lock)
                if taskItem:
                    curGroupId = taskItem["curGroupId"]
                    url = taskItem["url"]
                    utils.logInfo(f"==={curGroupId} begin", False)
                    utils.logInfo(f"==={curGroupId} GetTask: {taskItem}", False)
                    curDownloadDir, allCount = downloader.download(url, curGroupId)
                    taskItem["start_pts"] = calendar.timegm(time.gmtime())
                    taskItem["download_count"] = allCount
                    taskItem["download_dir"] = curDownloadDir
                    task.finishDownload(lock, taskItem)

            if self.type == task.C_STATE.TEMPLATEING and task.canTemplate(lock):
                taskItem = task.popTemplate(lock)
                if taskItem:
                    curGroupId = taskItem["curGroupId"]
                    curDownloadDir = taskItem["download_dir"]
                    utils.logInfo(f"==={curGroupId} processing video", False)
                    if taskItem["video_merge_num"] > 0 and taskItem["video_merge_second"] > 0:
                        # random cutter
                        utils.logInfo(f"==={curGroupId} random cutter ", False)
                        curDownloadDir = video_random_cutter.video_cutter(curDownloadDir, curGroupId, taskItem)
                    utils.logInfo(f"==={curGroupId} template video", False)
                    outputDir, processCount = processing.processToVideo(curDownloadDir, taskItem)
                    taskItem["processed_dir"] = outputDir
                    task.finishTemplate(lock, taskItem)

            if self.type == task.C_STATE.UPLOADING and task.canUpload(lock):
                taskItem = task.popUpload(lock)
                if taskItem:
                    curGroupId = taskItem["curGroupId"]
                    allCount = taskItem["download_count"]
                    processed_dir = taskItem["processed_dir"]
                    start_pts = taskItem["start_pts"]
                    utils.logInfo(f"==={curGroupId} uploading + notifying ", False)
                    uploadCount = uploading.upload(processed_dir, curGroupId)
                    current_pts = calendar.timegm(time.gmtime())
                    utils.logInfo(f"==={curGroupId} complate => {curGroupId} rst={uploadCount}/{allCount} duration={(current_pts - start_pts)}", False)
                    task.finishUpload(lock, taskItem)
                    clearDir(curGroupId)
            time.sleep(1)
    def markStop(self):
        self.running = False

def clearDir(curGroupId):
    downloader.clearDir(curGroupId)
    video_random_cutter.clearDir(curGroupId)
    processing.clearDir(curGroupId)

def canbeDownload():
    return downloader.downloadDirSubCount() < 3

def getTask():
    s = requests.session()
    s.headers.update({'Connection':'close'})
    res = s.get(f"https://beta.2tianxin.com/common/admin/tta/get_task?t={random.randint(100,99999999)}", verify=False)
    s.close()
    if len(res.content) > 0:
        data = json.loads(res.content)
        if len(data) > 0 and "id" in data:
            curGroupId = data["id"]
            url = data["url"].replace("\n", "").replace(";", "").replace(",", "").strip()
            template_name_list = data["template_name_list"]
            if template_name_list == None:
                template_name_list = []
            video_merge_num = int(data["video_merge_num"])
            video_merge_second = int(data["video_merge_second"])
            img_to_video = int(data["img_to_video"])
            split_video = int(data["split_video"])
            add_text = int(data["add_text"])
            tag = data["tag"]
            verticalScreen = False
            if "VerticalScreen=true" in url:
                verticalScreen = True
                url = url.replace("VerticalScreen=true","")
            return curGroupId, url, template_name_list, video_merge_num, video_merge_second, img_to_video, split_video, add_text, verticalScreen, tag
    return None, None, None, None, None, None, None, None, None, None

def autoCrawler():    
    thisFileDir = os.path.dirname(os.path.abspath(__file__))
    global THEADING_LIST
    for i in range(0, task.MAX_DOWNLOADING_COUNT):
        THEADING_LIST.append(CralwerThread(t=task.C_STATE.DOWNLOADING))
    for i in range(0, task.MAX_PROCESSING_COUNT):
        THEADING_LIST.append(CralwerThread(t=task.C_STATE.TEMPLATEING))
    for i in range(0, task.MAX_UPLOADING_COUNT):
        THEADING_LIST.append(CralwerThread(t=task.C_STATE.UPLOADING))
    THEADING_LIST.append(CralwerStateThread())
    while (os.path.exists(os.path.join(thisFileDir, "stop.now")) == False):
        if task.canAddDownload(lock):
            try:
                # task.push(lock, {
                #     "curGroupId":0, 
                #     "url":"ftp://192.168.3.220/1TB01/data/test/",
                #     "crawler_template_name":[], 
                #     "addRandomText":True, 
                #     "splitDuration":0, 
                #     "img_to_video":5,
                #     "video_merge_num":0,
                #     "video_merge_second":0, 
                #     "verticalScreen":False, 
                #     "tag":"bag"
                # })
                curGroupId, url, template_name_list, video_merge_num, video_merge_second, img_to_video, split_video, add_text, verticalScreen, tag = getTask()
                if curGroupId:    
                    task.push(lock, {
                        "curGroupId":curGroupId, 
                        "url":url,
                        "crawler_template_name":template_name_list, 
                        "addRandomText":add_text, 
                        "splitDuration":split_video, 
                        "img_to_video":img_to_video,
                        "video_merge_num":video_merge_num,
                        "video_merge_second":video_merge_second, 
                        "verticalScreen":verticalScreen, 
                        "tag":tag
                    })
            except Exception as e:
                utils.logInfo("====================== uncatch Exception ======================", False)
                utils.logInfo(e, False)
                utils.logInfo("======================      end      ======================", False)
        time.sleep(10)
    utils.logInfo(f"prepare stop !", False)
    for t in THEADING_LIST:
        t.markStop()
    for t in THEADING_LIST:
        t.join()
    os.remove(os.path.join(thisFileDir, "stop.now"))
    qyWechatRobot({
        "msgtype": "text",
        "text": {
            "content": f"爬虫机<{socket.gethostname()}> 下线"
        }
    })
    utils.logInfo(f"stoped !", False)

# urllib3.disable_warnings()
# logFilePath = f"{os.path.dirname(os.path.abspath(__file__))}/log.log"
# if os.path.exists(logFilePath) and os.stat(logFilePath).st_size > (1024 * 1024 * 5):  # 5m bak file
#     d = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
#     bakFile = logFilePath.replace(".log", f"_{d}.log")
#     shutil.copyfile(logFilePath, bakFile)
#     os.remove(logFilePath)
# logging.basicConfig(filename=logFilePath, 
#                     format='%(asctime)s %(levelname)s %(message)s',
#                     datefmt='%a, %d %b %Y %H:%M:%S',
#                     encoding="utf-8",
#                     level=logging.INFO)
# rootDir = os.path.dirname(os.path.abspath(__file__))

# data = {
#     "0":"'https://instagram.com/katy_closets?igshid=NTc4MTIwNjQ2YQ==",
# }

# # maxDownloadCount = 2
# splitZipCount = 100
# for k in data:
#     curGroupId = int(k)
#     allCount = 0
#     successCount = 0
#     start_pts = calendar.timegm(time.gmtime())
#     utils.logInfo(f"================ begin {curGroupId} ===================")
#     utils.logInfo(f"=== begin {curGroupId}")
#     url = data[k]
#     crawler_template_name = [ "template8" ] 
#     video_merge_num = 0
#     video_merge_second = 0
#     img_to_video = 4
#     split_video = 0
#     add_text = False
#     verticalScreen = False
#     process(url, crawler_template_name, add_text, split_video, img_to_video, video_merge_num, video_merge_second, verticalScreen)
#     current_pts = calendar.timegm(time.gmtime())
#     utils.logInfo(f"complate => {curGroupId} rst={successCount}/{allCount} duration={(current_pts - start_pts)}")
#     utils.logInfo(f"================ end {curGroupId} ===================")


# # utils.logInfo(os.stat("C:\\Users\\123\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\ttauto_crawler\\.download\\1573\\1573_2_11_0_autoremove_1.mp4").st_size)