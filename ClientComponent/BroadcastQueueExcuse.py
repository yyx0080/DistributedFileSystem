# 处理广播队列的消息
import requests

import pika
import os
import json
import base64
from MonitorFiles import FileComparison
# 连接 RabbitMQ 服务器
credentials = pika.PlainCredentials('Client1', 'yyx18259338897')    # 设置为自己的用户名 Unique
connection = pika.BlockingConnection(pika.ConnectionParameters('103.40.13.95',43222,'/',credentials))
channel = connection.channel()

# 声明一个名为 'file_broadcast2' 的队列 客户端2(湖北专用) Unique
channel.queue_declare(queue='file_broadcast1')
# 文件保存的本地路径
SAVE_FOLDER = 'C:/Users/yyx/Desktop/UploadFile'  # Unique
# 下载函数
def download_file_from_server(url, filename):
    # 构建文件的完整本地路径
    save_path = os.path.join(SAVE_FOLDER, filename)
    try:
        # 发送 HTTP GET 请求并下载文件
        response = requests.get(url)
        # 检查响应状态码是否为成功
        if response.status_code == 200:
            # 将文件内容写入本地文件
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f"File '{filename}' downloaded successfully.")
        else:
            print(f"Failed to download file '{filename}': Unexpected status code {response.status_code}")
    except Exception as e:
        print(f"Failed to download file '{filename}': {e}")
# 删除函数
def delete_file_self(del_path):
    if os.path.exists(del_path):
        os.remove(del_path)
        print("本地文件删除成功")
    else:
        print("未找到本地文件")
# 处理心跳的函数
def heart_receive(data):
    print("receive from server heart ： ",data)
# 处理字典函数，用作初始化和后续隔时同步
def filename_hash_receive(filename_hash_server):
    filename_hash_client = FileComparison.get_files_and_hashes(FileComparison.folder_path)
    # 比较服务器和本地的字典数据，找出差异
    server_only = set(filename_hash_server.keys()) - set(filename_hash_client.keys())  # 服务器有而本地没有的文件
    local_only = set(filename_hash_client.keys()) - set(filename_hash_server.keys())  # 本地有而服务器没有的文件
    common_files = set(filename_hash_server.keys()) & set(filename_hash_client.keys())  # 两边都有的文件
    # 对于两边都有的文件，比较哈希值，找出哈希值不同的文件
    different_hashes = [file for file in common_files if filename_hash_server[file] != filename_hash_client[file]]
    # 输出结果
    print("Files only on server:", server_only)
    print("Files only on local:", local_only)
    print("Files with different hashes:", different_hashes)
    # 删除本地有而服务器没有的文件
    for filename in local_only:
        os.remove(os.path.join(SAVE_FOLDER, filename))  # 使用 os.remove() 函数删除本地文件
    # 下载服务器有，但是本地没有的文件，两边都有，但是哈希值不同的文件
    for filename in server_only:
        url = 'http://103.40.13.95:58197/' + "download" + '/' + filename
        print("url = ", url)
        download_file_from_server(url, filename)
    for filename in different_hashes:
        url = 'http://103.40.13.95:58197/' + "download" + '/' + filename
        print("url = ", url)
        download_file_from_server(url, filename)


# 回调函数，处理接收到的文件内容
def callback(ch, method, properties, body):
    # 解析消息中的文件名和文件内容
    data = json.loads(body.decode())
    filename = data.get('filename')
    optype = data.get('type')   # 操作类型
    # 通过filename从服务器取得文件即可
    print(data)
    if 'add' in optype:
        url = 'http://103.40.13.95:58197/' + "download" + '/' + filename
        print("url = ",url)
        download_file_from_server(url,filename)
        # 发送确认消息
        ch.basic_ack(delivery_tag=method.delivery_tag)
    elif 'del' in optype:
        # 删除本地文件夹中的对应文件即可
        del_path = os.path.join(SAVE_FOLDER, filename)
        delete_file_self(del_path)
        # 发送确认消息
        ch.basic_ack(delivery_tag=method.delivery_tag)
    elif 'heartbeat' in optype:
        # 处理心跳
        heart_receive(data)
        # 发送确认消息
        ch.basic_ack(delivery_tag=method.delivery_tag)
    elif 'dict' in optype:
        # 处理字典
        filenamehash = data.get('dict')
        filename_hash_receive(filenamehash)
        # 发送确认消息
        ch.basic_ack(delivery_tag=method.delivery_tag)




# 监听队列，并注册回调函数
channel.basic_consume(queue='file_broadcast1', on_message_callback=callback)    # Unique

print('Waiting for files...')

# 开始监听队列
channel.start_consuming()
