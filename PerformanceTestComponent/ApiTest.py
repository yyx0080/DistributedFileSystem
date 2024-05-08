import matplotlib
import time
import matplotlib.pyplot as plt
import requests


# 定义接口地址
upload_url = 'http://103.40.13.95:58197/upload'
download_url = 'http://103.40.13.95:58197/download'
delete_url = 'http://103.40.13.95:58197/delete'
# 指定Matplotlib后端
matplotlib.use('TkAgg')  # 使用TkAgg后端，你也可以根据需要选择其他后端

# 测试上传文件接口性能
def test_upload_performance(file_path):
    start_time = time.time()
    with open(file_path, 'rb') as file:
        response = requests.post(upload_url, files={'file': file})
    end_time = time.time()
    return end_time - start_time

# 测试下载文件接口性能
def test_download_performance(file_name):
    start_time = time.time()
    response = requests.get(download_url, params={'file_name': file_name})
    end_time = time.time()
    return end_time - start_time

# 测试删除文件接口性能
def test_delete_performance(file_name):
    start_time = time.time()
    response = requests.post(delete_url, data={'file_name': file_name})
    end_time = time.time()
    return end_time - start_time

# 测试上传文件接口性能示例
file_path = 'test_file.txt'
upload_time = test_upload_performance(file_path)

# 测试下载文件接口性能示例
file_name = 'test_file.txt'
download_time = test_download_performance(file_name)

# 测试删除文件接口性能示例
delete_time = test_delete_performance(file_name)

# 可视化结果
labels = ['Upload', 'Download', 'Delete']
times = [upload_time, download_time, delete_time]

plt.bar(labels, times)
plt.ylabel('Time (seconds)')
plt.title('Performance of Cloud Server APIs')
plt.show()
