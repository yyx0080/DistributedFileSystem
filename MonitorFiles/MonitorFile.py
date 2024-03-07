#这个组件用来监控某个文件夹的修改情况
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # 当文件夹中有文件被修改时触发此方法
        print(f'File {event.src_path} has been modified')

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
    #监控文件是否修改
    folder_path = 'C:/Users/yyx/Desktop/UploadFile'  # 要监控的文件夹路径
    monitor_folder(folder_path)
