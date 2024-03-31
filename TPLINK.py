from tplink.sdk.TPOpenNative import SDKReqCallback, TPOpenNative, SDKPlayerCallbackContext
from tplink.sdk.IPCDevice import IPCDevice
from tplink.sdk.TPOpenNative import SDKReqCallback, TPOpenNative, SDKPlayerCallbackContext
from tplink.sdk.TPSDKContext import TPSDKContext
from tplink.sdk.TPPlayer import TPPlayer
from tplink.sdk.IPCDeviceContext import IPCDeviceContext
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import QThread
from UI_TPLINK import Ui_TPLINK
from datetime import datetime
import sys
import ctypes as __ctypes
import typing as __typing
import _ctypes as ___ctypes

import builtins as __builtins__
import os as os
import collections.abc as __collections_abc
import tplink.sdk.__init__


x = 0  # 定义X坐标
y = x  # 定义Y坐标
ctx = SDKPlayerCallbackContext()  # 实例化SDKPlayer回调函数


class InitIPC(QThread):
    """子线程初始化IPC并开启IPC预览"""

    def __init__(self, deviceContext):
        super().__init__()
        self.deviceContext = deviceContext  # 获取设备上下文

    def run(self):
        global x, y
        TPOpenNative.SDKAppReqStart(None, 0, 1)  # 开启APP底层
        TPOpenNative.SDKInitDevice(self.deviceContext, '172.18.7.13', 80)  # 初始化设备

        # 登录回调函数
        def loginCallBAck(a, status, b, c):
            if status.mError >= 0:
                # 获取设备能力集回调函数
                def getConnectCallBack(a, status, b, c):
                    if status.mError >= 0:
                        # 获取视频播放端口回调函数
                        def getVideoPort(a, status, b, c):
                            global SystemStatus
                            if status.mError >= 0:
                                # 调整摄像头坐标为(0,0)
                                TPOpenNative.SDKReqMotorMoveTo(self.deviceContext, None, 0, x, y, -1)

                        # 获取视频播放端口
                        TPOpenNative.SDKReqGetVideoPort(self.deviceContext, getVideoPort, 0)

                # 获取设备能力集
                TPOpenNative.SDKReqConnectDev(self.deviceContext, getConnectCallBack, 0)

        # 登录鉴权
        TPOpenNative.SDKReqLogin(self.deviceContext, loginCallBAck, 0, 'admin', '123456')


def ctrlIPC(deviceContext, xCoord, yCoord):
    """控制摄像头云台"""
    global x, y
    x = xCoord
    y = yCoord
    TPOpenNative.SDKReqMotorMoveTo(deviceContext, None, 0, x, y, -1)  # 控制云台旋转


class MainWindow(QWidget, Ui_TPLINK):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.deviceContext = TPOpenNative.SDKCreateDevice()  # 获取设备上下文
        self.tpPlayer = TPOpenNative.SDKCreatePlayer(ctx)  # 获取Player上下文
        self.winId = int(self.player.winId())
        self.ipcThread = InitIPC(self.deviceContext)  # 实例化初始化IPC子线程
        self.bind()  # 绑定视图
        self.ipcThread.start()

    def bind(self):
        """绑定试图,设置信号与槽"""
        global x, y
        self.startBtn.clicked.connect(self.startIPC)
        self.closeBtn.clicked.connect(self.stopIPC)
        self.upBtn.clicked.connect(lambda: ctrlIPC(self.deviceContext, x, y + 10))
        self.downBtn.clicked.connect(lambda: ctrlIPC(self.deviceContext, x, y - 10))
        self.leftBtn.clicked.connect(lambda: ctrlIPC(self.deviceContext, x - 10, y))
        self.rightBtn.clicked.connect(lambda: ctrlIPC(self.deviceContext, x + 10, y))
        self.snapshotBtn.clicked.connect(self.snapshot)
        self.startRecordBtn.clicked.connect(lambda: self.Record(0))
        self.stopRecordBtn.clicked.connect(lambda: self.Record(1))

    def snapshot(self):
        """截图"""
        filePath = "TPSnapshot_{}.jpg".format(datetime.now().strftime("%Y%m%d%H%M%S"))
        if TPOpenNative.SDKPlayerSnapshot(self.tpPlayer, filePath) >= 0:
            print(f"截图成功,文件路径为:{filePath}")
        else:
            print("截图失败")

    def Record(self, mod: int):
        """视频录制"""
        filePath = "TPSnapshot_{}.mp4".format(datetime.now().strftime("%Y%m%d%H%M%S"))
        if mod == 0:
            if TPOpenNative.SDKPlayerStartRecord(self.tpPlayer, filePath) >= 0:
                print(f"开始录制,文件路径为:{filePath}")
            else:
                print("开始录制失败")
        else:
            if TPOpenNative.SDKPlayerStopRecord(self.tpPlayer) >= 0:
                print(f"结束录制")
            else:
                print("结束录制失败")

    def startIPC(self):
        if self.tpPlayer is None:
            self.tpPlayer = TPOpenNative.SDKCreatePlayer(ctx)  # 获取Player上下文
        TPOpenNative.SDKPlayerStartPreview(self.tpPlayer, self.deviceContext, -1, 1, self.winId)  # 开启预览

    def stopIPC(self):
        """关闭IPC预览"""
        TPOpenNative.SDKPlayerStopPreview(self.tpPlayer)  # 关闭预览
        TPOpenNative.SDKDeletePlayer(self.tpPlayer)  # 销毁Player上下文
        self.tpPlayer = None  # 清空Player上下文
        self.player.clear()  # 清除Label内容


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
