# 本地客户端代码 local_client.py

import requests


def upload_file_to_cloud(file_path):
    # 指定云服务器的地址
    cloud_server_url = 'http://103.40.13.95:56725/upload'

    # 打开本地文件并读取内容
    with open(file_path, 'rb') as file:
        file_content = file.read()

    # 发送 POST 请求将文件内容上传到云服务器
    response = requests.post(cloud_server_url, data=file_content)

    # 打印服务器返回的响应结果
    print(response.text)


if __name__ == '__main__':
    # 上传本地文件到云服务器
    upload_file_to_cloud('C:/Users/yyx/Desktop/UploadFile/5464564.txt')