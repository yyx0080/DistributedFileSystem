import http.server
import os
import re
import threading

from ServerComponent import AddBroadcast
from MonitorFiles import FileComparison


can_upload = False
# 指定保存文件的目录
upload_dir = 'C:/Users/Administrator/Desktop/File'
class FileUploadDeleteModHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):

        content_length = int(self.headers['Content-Length'])
        file_content = self.rfile.read(content_length)

        # 获取文件名和哈希值
        filename = self.headers.get('X-File-Name')
        filehash = self.headers.get('X-File-Hash')
        print("hash = ",filehash)

        # 这里判断一下文件是否和服务器内部的文件一致
        # 一致性由两个决定，哈希值和名字
        # 先判断名字 再判断哈希
        # 如果一致就把标志位设置为false,表示不需要上传
        # 确定上传文件保存的目录
        # 获取服务器文件夹下所有文件的名称和哈希值
        files_and_hashes = FileComparison.get_files_and_hashes(FileComparison.folder_path)

        # 检查文件名是否存在于服务器文件夹下
        if filename not in files_and_hashes:
            # 如果文件名不存在，表示服务器上没有该文件，可以上传
            can_upload = True
        else:
            # 如果文件名存在，则检查哈希值是否一致
            server_hash = files_and_hashes[filename]
            if server_hash == filehash:
                # 如果哈希值一致，表示文件一致，不需要上传
                can_upload = False
            else:
                # 如果哈希值不一致，表示文件不一致，可以上传
                can_upload = True


        if can_upload == True:
            os.makedirs(upload_dir, exist_ok=True)

            # 保存上传的文件到指定目录
            with open(os.path.join(upload_dir, filename), 'wb') as f:
                f.write(file_content)

            # 返回上传成功的响应
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'File uploaded successfully')
            # 如果上传成功，就放入广播队列中
            fileSavePath = os.path.join(upload_dir, filename)   # 这个路径是刚刚上传文件的路径
            AddBroadcast.add_broupload_file(fileSavePath)
        else:
            print("文件已经存在了，名字为",filename)

    # 删除文件功能
    def do_DELETE(self):
        # 获取文件名
        filename = self.headers.get('X-File-Name')

        # 删除指定文件
        file_path = os.path.join(upload_dir, filename)
        print("deleteFilePath = ",file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f'File {filename} deleted successfully'.encode())
            fileDeletePath = os.path.join(upload_dir, filename)  # 这个路径是刚刚上传文件的路径
            AddBroadcast.del_brouload_file(fileDeletePath)
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f'File {filename} not found'.encode())


# 上传文件功能
def add_mod_del_File():
    server_address = ('', 25567)  # 这里端口要改成25567这个是雨云的安全组
    httpd = http.server.HTTPServer(server_address, FileUploadDeleteModHandler)
    print('Starting Center server...')
    httpd.serve_forever()
