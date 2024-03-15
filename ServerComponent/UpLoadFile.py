import http.server
import os
import re
from ServerComponent import AddBroadcast
class FileUploadHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        file_content = self.rfile.read(content_length)

        # 获取文件名
        filename = self.headers.get('X-File-Name')

        # 指定保存文件的目录
        upload_dir = 'C:/Users/Administrator/Desktop/File'
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
# 上传文件功能
def add_File():
    server_address = ('', 25567)  # 这里端口要改成25567这个是雨云的安全组
    httpd = http.server.HTTPServer(server_address, FileUploadHandler)
    print('Starting ADD server...')
    httpd.serve_forever()
