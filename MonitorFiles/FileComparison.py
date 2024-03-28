# 用于文件比较的功能
import os
import hashlib

# 调用函数获取文件夹内所有文件的名字和哈希值
folder_path = 'C:/Users/yyx/Desktop/UploadFile' # Unique

def get_files_and_hashes(folder_path):
    files_and_hashes = {}

    # 遍历文件夹内所有文件
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            # 计算文件的哈希值
            hash_value = hash_file(file_path)
            # 将文件名和哈希值添加到字典中
            files_and_hashes[file] = hash_value

    return files_and_hashes

def hash_file(file_path):
    # 创建哈希对象
    hasher = hashlib.md5()
    # 以二进制读取文件内容，并更新哈希对象
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(65536)  # 64 KB 每次读取的数据块大小
            if not data:
                break
            hasher.update(data)
    # 返回文件的哈希值
    return hasher.hexdigest()


# files_and_hashes = get_files_and_hashes(folder_path)
#
# # 打印结果
# for file, hash_value in files_and_hashes.items():
#     print(f'File: {file}, Hash: {hash_value}')
