import time

import pika
import os
import json
import base64
# 保证服务器端启动了RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',heartbeat=0))
channel = connection.channel()

# 声明一个名为 'file_broadcast2' 的队列 湖北，一一对应
# 同时，这个队列，包含上传文件，修改文件，删除文件等信息
channel.queue_declare(queue='file_broadcast1')  # 宿舍电脑
channel.queue_declare(queue='file_broadcast2')  # 湖北客户端


# 定义文件上传函数
# 这个函数后面增加一个标志位，标志哪一个客户端发送
# 那么这个客户端就不用把数据送入消息队列中
def add_broupload_file(file_path):
    filename = os.path.basename(file_path)
    # 组装消息
    optype = "add"
    message = {
        'filename': filename,
        'type': optype,
        'from': 123
    }
    # 发送文件内容到队列
    # 这里后面要多次调用，就是不用调用谁发送的消息队列，谁发送的，他的消息队列就不调用
    channel.basic_publish(exchange='', routing_key='file_broadcast1', body=json.dumps(message))
    channel.basic_publish(exchange='', routing_key='file_broadcast2', body=json.dumps(message))
    print("File '{}' uploaded add_file_broadcast1 successfully.".format(filename))
    print("File '{}' uploaded add_file_broadcast2 successfully.".format(filename))

# 定义删除文件函数
# 把删除信息丢入消息队列中
def del_brouload_file(file_path):
    filename = os.path.basename(file_path)
    # 组装消息
    optype = "del"
    message = {
        'filename': filename,
        'type': optype,
        'from': 123
    }
    # 发送文件内容到队列
    # 这里后面要多次调用，就是不用调用谁发送的消息队列，谁发送的，他的消息队列就不调用
    channel.basic_publish(exchange='', routing_key='file_broadcast1', body=json.dumps(message))
    channel.basic_publish(exchange='', routing_key='file_broadcast2', body=json.dumps(message))
    print("File '{}' del add_file_broadcast1 successfully.".format(filename))
    print("File '{}' del add_file_broadcast2 successfully.".format(filename))

# 新增一个方法，持续给客户端发送心跳
def send_heartbeat():
    while True:
        optype = "heartbeat"
        filename = "serverHeartBeat"
        message = {
            'filename': filename,
            'type': optype,
            'from': 123
        }
        # 发送文件内容到队列
        # 这里后面要多次调用，就是不用调用谁发送的消息队列，谁发送的，他的消息队列就不调用
        channel.basic_publish(exchange='', routing_key='file_broadcast1', body=json.dumps(message))
        channel.basic_publish(exchange='', routing_key='file_broadcast2', body=json.dumps(message))
        print("File '{}' heart add_file_broadcast1 successfully.")
        print("File '{}' heart add_file_broadcast2 successfully.")
        # 休眠10s
        time.sleep(10)

# 用来获取本地File的所有文件名称以及哈希值，用于初始化
def send_filename_hash(files_and_hashes,address):
    # 组装消息
    filename = "dict"
    optype = "dict"
    message = {
        'filename': filename,
        'type': optype,
        'from': 123,
        'dict': files_and_hashes
    }
    if "117.30.183.237" in address:
        print("is PC from dormitory")
        # 发送消息队列到宿舍的电脑
        channel.basic_publish(exchange='', routing_key='file_broadcast1', body=json.dumps(message))
    else:
        print("unKnow ip address error!")
