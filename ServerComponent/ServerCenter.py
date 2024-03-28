import socket
import threading
import time
from ServerComponent import UpLoadFile
from ServerComponent import AddBroadcast
from MonitorFiles import FileComparison
# 监听地址和端口
host = '0.0.0.0'  # 服务器IP地址，'0.0.0.0'表示监听所有可用的网络接口
port = 58528      # 服务器端口号

# 存储客户端信息的字典
clients = {}

# 创建一个 TCP/IP 套接字
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 设置地址复用，为的是断后重新链接
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# 绑定地址和端口
server_socket.bind((host, port))

# 开始监听连接
server_socket.listen(20)

print('Waiting for connections...')

def handle_client(client_socket, address):
    try:
        print('Connection from', address)
        # 这里初始化一次
        filename_hash = FileComparison.get_files_and_hashes(FileComparison.folder_path)
        AddBroadcast.send_filename_hash(filename_hash, address)
        # 存储客户端信息（用于心跳）
        clients[address] = client_socket
        # 接收和处理客户端消息
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print('Received from', address, ':', data.decode())

            if data == b'CLOSE':
                break
            client_socket.sendall(b'Hello from server!')

    finally:
        # 关闭连接
        client_socket.close()
        print('Connection closed by', address)
        # 移除客户端信息
        del clients[address]

# 监听客户端心跳
def monitor_clients():
    while True:
        for address, client_socket in list(clients.items()):
            try:
                # 发送心跳消息
                client_socket.sendall(b'heartbeat')

            except:
                # 处理异常（客户端断开连接）
                print('Client', address, 'disconnected')
                # 关闭客户端连接
                client_socket.close()
                # 移除客户端信息
                del clients[address]
        # 休眠一段时间，这里要改成很久很久检测一次3600s
        time.sleep(60)
        # ADD功能
        # MOD功能
        # DEL功能
        threading.Thread(target=UpLoadFile.add_mod_del_File()).start()


def StartServer():
    # 启动客户端心跳监控线程
    threading.Thread(target=monitor_clients).start()
    while True:
        # 接受客户端连接
        client_socket, address = server_socket.accept()
        # 启动一个线程来处理客户端连接
        threading.Thread(target=handle_client, args=(client_socket, address)).start()
        #threading.Thread(target=UpLoadFile.add_File()).start()  # 这行代码有问题要删掉
