# 展示File内容的网页
from flask import Flask, render_template, send_from_directory, redirect, url_for
import os
from urllib import request
app = Flask(__name__)
UPLOAD_FOLDER = 'C:/Users/Administrator/Desktop/File'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    # 获取文件夹内的所有文件名

    files = os.listdir(UPLOAD_FOLDER)
    file_sizes = {}
    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file)
        file_size_kb = os.path.getsize(file_path) / 1024  # Convert bytes to KB
        file_sizes[file] = f"{file_size_kb:.2f} KB"  # Format to two decimal places
    return render_template('index.html', files=files,file_sizes=file_sizes)

@app.route('/download/<filename>')
def download_file(filename):
    # 从指定文件夹提供文件下载
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # 检查是否有文件被上传
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # 如果用户没有选择文件，浏览器会提交一个没有文件名的空文件
        if file.filename == '':
            return redirect(request.url)
        if file:
            # 保存上传的文件到指定文件夹
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return redirect(url_for('index'))
    else:
        return "File not found"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=25565,debug=True)
