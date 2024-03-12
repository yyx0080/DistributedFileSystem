# 展示File内容的网页
from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'C:/Users/Administrator/Desktop/File'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    # 获取文件夹内的所有文件名
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', files=files)

@app.route('/download/<filename>')
def download_file(filename):
    # 从指定文件夹提供文件下载
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=25565,debug=True)
