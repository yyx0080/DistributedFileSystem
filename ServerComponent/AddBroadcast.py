import pika
import os
import json
import base64
# 保证服务器端启动了RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 声明一个名为 'file_broadcast2' 的队列 湖北，一一对应
# 同时，这个队列，包含上传文件，修改文件，删除文件等信息
channel.queue_declare(queue='file_broadcast2')

# 定义文件上传函数
# 这个函数后面增加一个标志位，标志哪一个客户端发送
# 那么这个客户端就不用把数据送入消息队列中
def add_broupload_file(file_path):
    filename = os.path.basename(file_path)
    with open(file_path, 'rb') as file:
        file_content = file.read()
        # 使用 Base64 编码将字节类型转换为字符串类型
        file_content_base64 = base64.b64encode(file_content).decode('utf-8')
        # 组装消息
        message = {
            'filename': filename,
            'file_content': file_content_base64
        }
        # 发送文件内容到队列
        # 这里后面要多次调用，就是不用调用谁发送的消息队列，谁发送的，他的消息队列就不调用
        channel.basic_publish(exchange='', routing_key='file_broadcast2', body=json.dumps(message))
    print("File '{}' uploaded add_file_broadcas2t successfully.".format(filename))


