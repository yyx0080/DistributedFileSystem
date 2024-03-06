import socket

# 服务器地址和端口
server_address = '103.40.13.95'  # 云服务器的IP地址
server_port = 59748                 # 服务器端口号

# 创建一个 TCP/IP 套接字
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # 连接服务器
    client_socket.connect((server_address, server_port))

    # 发送和接收数据
    while True:
        # 发送数据
        message = 'Hello from client!'
        client_socket.sendall(message.encode())

        # 接收数据
        data = client_socket.recv(1024)
        print('Received:', data.decode())
finally:
    # 关闭连接
    client_socket.close()
