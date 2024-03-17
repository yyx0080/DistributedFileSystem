import socket
import threading
import time
from MonitorFiles import MonitorFile

# 服务器地址和端口
server_address = '103.40.13.95'  # 云服务器的IP地址
server_port = 59748                 # 服务器端口号


# 创建一个 TCP/IP 套接字
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def send_heartbeat():
    while True:
        try:
            # 发送心跳消息
            client_socket.sendall(b'heartbeat')
            time.sleep(10)  # 每分钟发送一次心跳消息
        except:
            break


def receive_heartbeat():
    while True:
        try:
            # 接收心跳消息
            data = client_socket.recv(1024)
            if not data:
                break
            print('Received heartbeat from server:', data.decode())
        except:
            break

def StartClient():
    try:
        # 连接服务器
        client_socket.connect((server_address, server_port))

        # 启动发送和接收心跳消息的线程
        threading.Thread(target=send_heartbeat).start()
        threading.Thread(target=receive_heartbeat).start()
        # 启动监控本地文件线程
        threading.Thread(targe=MonitorFile.MonitorChange()).start()
        # 增删改由不同的线程来实现



        # 发送和接收数据
        while True:
            pass
    finally:
        # 关闭连接
        # 在客户端关闭时向服务器发送关闭消息
        client_socket.sendall(b'CLOSE')
        client_socket.close()
