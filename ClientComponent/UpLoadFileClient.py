import threading
import requests
from MonitorFiles import MonitorFile

def upload_file_to_cloud(file_path):
    # 指定云服务器的地址
    cloud_server_url = 'http://103.40.13.95:56725/upload'

    # 构造包含文件的字典
    files = {'file': open(file_path, 'rb')}

    # 发送 POST 请求将文件内容上传到云服务器
    response = requests.post(cloud_server_url, files=files)

    # 打印服务器返回的响应结果
    print(response.text)


# if __name__ == '__main__':
#     # 上传本地文件到云服务器
#     upload_file_to_cloud('C:/Users/yyx/Desktop/UploadFile/5464564.txt')
