# 这个组件用来监控某个文件夹的修改情况
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
# 这里要导入多个包，增 删 改
# ADD
from ClientComponent import UpLoadFileClient
from ClientComponent import DeleteFileClient
class MyHandler(FileSystemEventHandler):
    def __init__(self):
        self.created_files = set()  # 用于存储已创建的文件路径

    def on_modified(self, event):
        # 当文件夹中有文件被修改时触发此方法
        if event.src_path not in self.created_files:
            print(f'File {event.src_path} has been modified')
            #这里上传文件即可


    def on_created(self, event):
        # 当文件夹中有新文件被创建时触发此方法
        self.created_files.add(event.src_path)
        print(f'File {event.src_path} has been created')
        # 这里上传文件即可
        UpLoadFileClient.upload_file_to_cloud(event.src_path)
    def on_deleted(self, event):
        # 当文件夹中有文件被删除时触发此方法
        print(f'File {event.src_path} has been deleted')
        DeleteFileClient.delete_file_on_cloud(event.src_path)

def monitor_folder(folder_path):
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def MonitorChange():
    # 监控文件是否修改
    folder_path = 'C:/Users/yyx/Desktop/UploadFile'  # 要监控的文件夹路径，需要定制化修改 Unique
    monitor_folder(folder_path)
