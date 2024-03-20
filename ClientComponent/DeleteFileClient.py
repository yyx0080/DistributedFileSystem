import os
import stat
import threading
import requests
from MonitorFiles import MonitorFile

def delete_file_on_cloud(file_path):
    cloud_server_url = 'http://103.40.13.95:56725/delete'
    filename = os.path.basename(file_path)
    file_path = file_path.replace('\\', '/')
    headers = {'X-File-Name': filename}
    print("delete file = ",filename)
    # 修改文件权限
    # os.chmod(file_path, stat.S_IRWXU)  # 防止出现[Errno 13] Permission denied
    # 检查文件的权限状态
    try:
        response = requests.delete(cloud_server_url, headers=headers)
        print(response.text)
    except IOError as e:
        print("Error:", e)
