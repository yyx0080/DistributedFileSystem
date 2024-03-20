import os
import stat
import threading
import requests
from MonitorFiles import MonitorFile

def delete_file_on_cloud(file_path):
    cloud_server_url = 'http://103.40.13.95:56725/delete'
    filename = os.path.basename(file_path)
    print("filepath = ", file_path)
    file_path = file_path.replace('\\', '/')
    print("filepath = ", file_path)
    headers = {'X-File-Name': filename}
    # 修改文件权限
    # os.chmod(file_path, stat.S_IRWXU)  # 防止出现[Errno 13] Permission denied
    # 检查文件的权限状态
    if os.access(file_path, os.W_OK):
        print("文件具有写入权限")
    else:
        print("文件没有写入权限")
    try:
        response = requests.post(cloud_server_url, headers=headers)
        print(response.text)
    except IOError as e:
        print("Error:", e)

# 删除云服务器上的文件
delete_file_on_cloud('C:/Users/yyx/Desktop/UploadFile/5464564.txt')