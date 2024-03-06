#这个用于建立链接，确保链接上了客户端
import socket

# 监听地址和端口
host = '0.0.0.0'  # 服务器IP地址，'0.0.0.0'表示监听所有可用的网络接口
port = 58528      # 服务器端口号

# 创建一个 TCP/IP 套接字
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定地址和端口
server_socket.bind((host, port))

# 开始监听连接
server_socket.listen(1)

print('Waiting for a connection...')
connection, client_address = server_socket.accept()

try:
    print('Connection from', client_address)

    while True:
        data = connection.recv(1024)
        if data:
            print('Received:', data.decode())
            connection.sendall(b'Hello from server!')
        else:
            break
finally:
    # 关闭连接
    connection.close()

