# 处理广播队列的消息
import pika
import os
import json
import base64
# 连接 RabbitMQ 服务器
credentials = pika.PlainCredentials('Client2', 'yyx18259338897')    # 设置为自己的用户名 Unique
connection = pika.BlockingConnection(pika.ConnectionParameters('103.40.13.95',43222,'/',credentials))
channel = connection.channel()

# 声明一个名为 'file_broadcast2' 的队列 客户端2(湖北专用)
channel.queue_declare(queue='file_broadcast2')

# 回调函数，处理接收到的文件内容
def callback(ch, method, properties, body):
    # 解析消息中的文件名和文件内容
    data = json.loads(body.decode())
    filename = data.get('filename')
    file_content_base64 = data.get('file_content')
    file_content = base64.b64decode(file_content_base64)    # 解码

    # 保存文件到本地
    if filename and file_content:
        with open('C:/Users/Administrator/Desktop/FileClient2/' + filename, 'wb') as file:
            file.write(file_content)
        print("File '{}' received from RabbitMQ successfully.".format(filename))
    else:
        print("Received message does not contain filename or file content.")

    # 发送确认消息
    ch.basic_ack(delivery_tag=method.delivery_tag)

# 监听队列，并注册回调函数
channel.basic_consume(queue='file_broadcast2', on_message_callback=callback)

print('Waiting for files...')

# 开始监听队列
channel.start_consuming()
