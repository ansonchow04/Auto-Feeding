from .MvImport.MvCameraControl_class import *


class Camera:
    """海康威视相机封装库"""
    
    def __init__(self):
        """初始化相机并打开第一个检测到的设备"""
        self.camera = None
        self._initialized = False
        
        # 初始化SDK
        MvCamera.MV_CC_Initialize()
        
        # 枚举设备
        device_list = MV_CC_DEVICE_INFO_LIST()
        ret = MvCamera.MV_CC_EnumDevices(MV_GIGE_DEVICE | MV_USB_DEVICE, device_list)
        
        if ret != MV_OK:
            raise RuntimeError(f"枚举设备失败，错误码: {ret}")
        
        if device_list.nDeviceNum == 0:
            raise RuntimeError("未找到任何相机设备")
        
        # 创建并打开第一个设备
        self.camera = MvCamera()
        dev_info = device_list.pDeviceInfo[0].contents
        
        ret = self.camera.MV_CC_CreateHandle(dev_info)
        if ret != MV_OK:
            raise RuntimeError(f"创建设备句柄失败，错误码: {ret}")
        
        ret = self.camera.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
        if ret != MV_OK:
            raise RuntimeError(f"打开设备失败，错误码: {ret}")
        
        # 设置触发模式为关闭（连续采集）
        ret = self.camera.MV_CC_SetEnumValue("TriggerMode", MV_TRIGGER_MODE_OFF)
        if ret != MV_OK:
            raise RuntimeError(f"设置触发模式失败，错误码: {ret}")
        
        # 开始取流
        ret = self.camera.MV_CC_StartGrabbing()
        if ret != MV_OK:
            raise RuntimeError(f"开始取流失败，错误码: {ret}")
        
        self._initialized = True
    
    def save(self, filename="photo.bmp", timeout=2000):
        """
        保存一张照片
        
        参数:
            filename: 保存的文件名，默认 "photo.bmp"
            timeout: 超时时间(毫秒)，默认 2000
            
        返回:
            成功返回True，失败抛出异常
        """
        if not self._initialized:
            raise RuntimeError("相机未初始化")
        
        # 获取图像缓冲区大小
        stParam = MVCC_INTVALUE()
        ret = self.camera.MV_CC_GetIntValue("PayloadSize", stParam)
        if ret != MV_OK:
            raise RuntimeError(f"获取图像大小失败，错误码: {ret}")
        
        # 创建缓冲区并获取一帧图像
        pData = (c_ubyte * stParam.nCurValue)()
        stFrameInfo = MV_FRAME_OUT_INFO_EX()
        
        ret = self.camera.MV_CC_GetOneFrameTimeout(pData, stParam.nCurValue, stFrameInfo, timeout)
        if ret != MV_OK:
            raise RuntimeError(f"获取图像帧失败，错误码: {ret}")
        
        # 准备保存参数
        stSaveParam = MV_SAVE_IMAGE_PARAM_EX()
        stSaveParam.enImageType = MV_Image_Bmp
        stSaveParam.enPixelType = stFrameInfo.enPixelType
        stSaveParam.nWidth = stFrameInfo.nWidth
        stSaveParam.nHeight = stFrameInfo.nHeight
        stSaveParam.nDataLen = stFrameInfo.nFrameLen
        stSaveParam.pData = cast(pData, POINTER(c_ubyte))
        
        # 输出缓冲区（BMP需要更大的缓冲区）
        pImageBuf = (c_ubyte * (stFrameInfo.nWidth * stFrameInfo.nHeight * 4))()
        stSaveParam.pImageBuffer = cast(pImageBuf, POINTER(c_ubyte))
        stSaveParam.nBufferSize = stFrameInfo.nWidth * stFrameInfo.nHeight * 4
        
        # 保存为BMP
        ret = self.camera.MV_CC_SaveImageEx2(stSaveParam)
        if ret != MV_OK:
            raise RuntimeError(f"保存图像失败，错误码: {ret}")
        
        # 写入文件
        try:
            with open(filename, 'wb') as f:
                f.write(bytearray(pImageBuf[0:stSaveParam.nImageLen]))
        except Exception as e:
            raise RuntimeError(f"写入文件失败: {e}")
        
        return True
    
    def close(self):
        """关闭相机并释放资源"""
        if self.camera and self._initialized:
            self.camera.MV_CC_StopGrabbing()
            self.camera.MV_CC_CloseDevice()
            self.camera.MV_CC_DestroyHandle()
            self._initialized = False
        
        MvCamera.MV_CC_Finalize()
    
    def __enter__(self):
        """支持 with 语句"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """自动关闭资源"""
        self.close()
        return False
    
    def __del__(self):
        """析构时自动清理"""
        self.close()
