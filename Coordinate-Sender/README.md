# 机器人坐标发送服务器

一个用于丽宫自动上料系统的 TCP 服务器，负责接收机器人连接并按需发送三维坐标数据。

## 📋 项目概述

本项目实现了一个基于 TCP 协议的服务器，用于与机器人客户端通信。服务器维护一个坐标队列，当接收到机器人发送的 `send location` 命令时，自动发送下一个坐标点。

## ✨ 主要特性

- **自动连接管理**：支持机器人断线重连，无需手动重启服务
- **坐标队列管理**：FIFO（先进先出）队列，依次发送坐标
- **坐标验证**：自动验证坐标格式和取值范围
- **异常处理**：完善的错误处理和连接恢复机制
- **实时日志**：详细的运行日志，便于调试和监控

## 🔧 坐标规范

坐标格式为三维列表 `[x, y, z]`，取值范围：
- **x 轴**：0 ~ 100
- **y 轴**：0 ~ 100  
- **z 轴**：-100 ~ 0

## 🚀 快速开始

### 基本使用

```python
from RobotServer import RobotServer

# 创建服务器实例
server = RobotServer(host='0.0.0.0', port='8080')

# 启动服务器
server.start()

# 添加坐标到队列
server.coords_append([100, 100, -100])
server.coords_append([100, 100, -75])
server.coords_append([100, 100, -50])

# 运行服务器主循环
while True:
    server.run_once()
```

### 完整示例

```python
import time
from RobotServer import RobotServer

if __name__ == "__main__":
    # 初始化服务器
    server = RobotServer(port='8080')
    server.start()
    
    # 预设坐标序列
    coordinates = [
        [100, 100, -100],
        [100, 100, -75],
        [100, 100, -50],
        [100, 100, -25]
    ]
    
    # 添加坐标到队列
    for coord in coordinates:
        server.coords_append(coord)
    
    # 查看当前队列
    server.coords_print()
    
    # 启动主循环
    try:
        while True:
            server.run_once()
            time.sleep(0.1)  # 避免 CPU 占用过高
    except KeyboardInterrupt:
        print("\n正在关闭服务器...")
        server.close_server()
```

## 📚 API 文档

### 类：`RobotServer`

#### 初始化参数
```python
RobotServer(host='0.0.0.0', port='8080', recv_buffer=1024)
```
- `host`: 监听地址，默认 `0.0.0.0` 监听所有网卡
- `port`: 监听端口，默认 `8080`
- `recv_buffer`: 接收缓冲区大小，默认 1024 字节

#### 主要方法

**`start()`**  
启动服务器并开始监听连接

**`coords_append(coord)`**  
添加坐标到队列
- 参数：`coord` - 格式为 `[x, y, z]` 的列表
- 返回：无
- 说明：会自动验证坐标格式和范围

**`coords_pop(index=0)`**  
取出并删除指定位置的坐标
- 参数：`index` - 坐标索引，默认为 0（队首）
- 返回：坐标列表或 None

**`coords_print()`**  
打印当前队列中的所有坐标

**`send_coord()`**  
发送队列中的下一个坐标给机器人

**`run_once()`**  
执行一次事件循环，处理接收消息和发送坐标

**`close_conn()`**  
关闭当前客户端连接

**`close_server()`**  
关闭服务器

## 🔌 通信协议

### 客户端 → 服务器
机器人客户端发送命令：
```
send location
```

### 服务器 → 客户端
服务器响应坐标数据：
```python
[100, 100, -100]
```

## ⚙️ 配置说明

### 网络配置
- 使用 `0.0.0.0` 作为监听地址可接受任何网卡的连接
- 确保机器人客户端与服务器在同一网段内
- 默认端口 `8080`，可根据需要修改

### 防火墙设置
确保防火墙允许指定端口的 TCP 入站连接：
```powershell
# Windows 防火墙规则示例
netsh advfirewall firewall add rule name="Robot Server" dir=in action=allow protocol=TCP localport=8080
```

## 📝 注意事项

1. **端口占用**：启动前确保端口未被其他程序占用
2. **坐标范围**：添加坐标前会自动验证，超出范围的坐标会被拒绝
3. **队列管理**：坐标按照添加顺序依次发送（FIFO）
4. **断线重连**：机器人断线后服务器会自动等待重连，无需重启
5. **资源释放**：程序退出前建议调用 `close_server()` 释放资源

## 🛠️ 依赖要求

- Python 3.6+
- 标准库：`socket`, `ast`, `time`

无需安装第三方依赖包。

## 📂 项目结构

```
Coordinate-Sender/
├── RobotServer.py    # 服务器核心类
├── example.py        # 使用示例
└── README.md         # 项目文档
```

## 🐛 故障排除

### 问题：服务器无法启动
- 检查端口是否被占用：`netstat -ano | findstr :8080`
- 尝试更换其他端口

### 问题：机器人无法连接
- 确认防火墙设置
- 检查网络连通性：`ping <服务器IP>`
- 验证机器人配置的 IP 和端口是否正确

### 问题：坐标发送失败
- 检查坐标格式是否正确
- 确认坐标值在允许范围内
- 查看服务器日志输出

## 📄 许可证

本项目为丽宫自动上料系统内部使用项目。

## 📮 联系方式

如有问题或建议，请联系项目维护团队。

---

**最后更新时间**：2025年12月22日

