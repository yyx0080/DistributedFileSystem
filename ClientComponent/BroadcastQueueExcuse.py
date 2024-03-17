# 处理广播队列的消息
import requests

import pika
import os
import json
import base64
# 连接 RabbitMQ 服务器
credentials = pika.PlainCredentials('Client2', 'yyx18259338897')    # 设置为自己的用户名 Unique
connection = pika.BlockingConnection(pika.ConnectionParameters('103.40.13.95',43222,'/',credentials))
channel = connection.channel()

# 声明一个名为 'file_broadcast2' 的队列 客户端2(湖北专用) Unique
channel.queue_declare(queue='file_broadcast2')
# 文件保存的本地路径
SAVE_FOLDER = 'C:/Users/Administrator/Desktop/FileClient2'  # Unique
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
# 回调函数，处理接收到的文件内容
def callback(ch, method, properties, body):
    # 解析消息中的文件名和文件内容
    data = json.loads(body.decode())
    filename = data.get('filename')
    # 通过filename从服务器取得文件即可
    print(data)
    url = 'http://103.40.13.95:58197/' + "download" + '/' + filename
    print("url = ",url)
    download_file_from_server(url,filename)
    # 发送确认消息
    ch.basic_ack(delivery_tag=method.delivery_tag)

# 监听队列，并注册回调函数
channel.basic_consume(queue='file_broadcast2', on_message_callback=callback)

print('Waiting for files...')

# 开始监听队列
channel.start_consuming()
