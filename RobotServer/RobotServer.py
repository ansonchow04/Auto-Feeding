import socket
import ast
import time

class RobotServer:
    def __init__(self, host='0.0.0.0', port='8080', recv_buffer=1024):
        self.host = host
        self.port = int(port)
        self.recv_buffer = recv_buffer
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(1.0)
        self.conn = None
        self.addr = None
        self.coords = list()

    def coords_append(self, coord_to_add):
        """添加坐标，格式为[x, y, z]，x和y取值0~100，z取值-100~0"""
        if isinstance(coord_to_add, list) and len(coord_to_add) == 3 \
        and coord_to_add[0] in range(0, 101) and coord_to_add[1] in range(0, 101) and coord_to_add[2] in range(-100, 1):
            self.coords.append(coord_to_add)
        else:
            print("Invalid coordinate:", coord_to_add)
    
    def coords_pop(self, index=0):
        """取出坐标并自动删除"""
        if len(self.coords) == 0:
            print("No coordinates to pop")
            return None
        return self.coords.pop(index)
    
    def coords_print(self):
        """打印所有坐标"""
        for i, coord in enumerate(self.coords):
            print(f"Coordinate {i}: {coord}")

    def start(self):
        """开启服务器并等待连接"""
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        print(f"Server listening on {self.host}:{self.port}")

    def close_conn(self):
        """关闭当前连接"""
        if self.conn:
            self.conn.close()
            self.conn = None
            print("Connection closed")

    def close_server(self):
        """关闭服务器连接"""
        if self.conn:
            self.conn.close()
            self.conn = None
        self.sock.close()
        print("Server closed")

    def recv_message(self, timeout=None):
        """尝试接收消息，若无消息则返回None"""
        if not self.conn:
            raise ConnectionError("No active connection")
        if timeout:
            self.conn.settimeout(timeout)
        try:
            data = self.conn.recv(self.recv_buffer)
            if not data:
                raise ConnectionError("Robot disconnected")
            return data.decode().strip()
        except socket.timeout:
            return None
        except ConnectionResetError:
            raise ConnectionError("Connection reset by Robot")
    
    def send_coord(self):
        """发送坐标给机器人"""
        if not self.conn:
            raise ConnectionError("No active connection")
        coords = self.coords_pop()
        if coords is None:
            print("No coordinates to send")
            return
        message = str(coords).encode()
        self.conn.sendall(message)
        print(f"Sent coordinates: {coords}")
        
    def run_once(self):
        try:
            message = self.recv_message(timeout=1)
            if message is None:
                return

            if message.lower() == 'send location':
                print("Received 'send location' command")
                self.send_coord()
            else:
                print("Unknown command:", message)

        except ConnectionError as e:
            print(e)
            # 只关 client，不关 server
            self.close_conn()
            print("Waiting for robot to reconnect...")
            while self.conn is None:
                try:
                    self.conn, self.addr = self.sock.accept()
                    print(f"Reconnected from {self.addr}")
                except socket.timeout:
                    pass

if __name__ == "__main__":
    server = RobotServer(port='8080')
    server.start()
    server.coords_append([100, 100, -100])
    server.coords_append([100, 100, -75])
    server.coords_append([100, 100, -50])
    server.coords_append([100, 100, -25])
    while True:
        server.run_once()
        
        time.sleep(1)
    