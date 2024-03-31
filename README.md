# TPLink IPC 控制程序

这是一个基于TP_OpenSDK和QT库开发的程序，用于控制TPLink网络摄像头。

## 功能

- 控制摄像头云台的旋转
- 视频预览
- 截图
- 视频录制

## 使用方法

1. 首先，你需要初始化IPC并开启IPC预览。你可以通过创建`InitIPC`类的实例并调用`start()`方法来完成这个操作。

```python
self.ipcThread = InitIPC(self.deviceContext)  # 实例化初始化IPC子线程
self.ipcThread.start()    # 启动子线程
```

2. 控制摄像头云台的旋转。你可以通过调用`ctrlIPC`函数并传入设备上下文和x、y坐标来控制摄像头云台的旋转。

```python
ctrlIPC(self.deviceContext, xCoord, yCoord)
```

3. 截图。你可以通过调用`snapshot`方法来进行截图。

```python
self.snapshot()
```

4. 视频录制。你可以通过调用`Record`方法并传入模式参数来进行视频录制。模式参数为0表示开始录制，为1表示结束录制。

```python
self.Record(mod)
```

## 注意事项

- 请确保你的设备上下文和Player上下文已经正确初始化。
- 请确保你的设备已经连接到网络，并且IP地址、端口、用户名和密码都是正确的。
