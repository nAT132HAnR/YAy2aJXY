# 代码生成时间: 2025-09-19 19:25:42
import os
import zipfile
from sanic import Sanic, response
from sanic.exceptions import ServerError
from sanic.request import Request
from sanic.response import json

# 创建Sanic应用
app = Sanic('FileDecompressionService')

# 定义错误处理函数
@app.exception(ServerError)
async def handle_server_error(request: Request, exception: Exception):
    return response.json({'error': str(exception)}, status=500)

# 定义压缩文件解压接口
@app.route('/api/decompress', methods=['POST'])
async def decompress_file(request: Request):
    # 从请求中获取文件
    file = request.files.get('file')
    if not file:
        return response.json({'error': 'No file provided'}, status=400)

    try:
        # 确保文件是ZIP格式
        if file.name.split('.')[-1] != 'zip':
            return response.json({'error': 'Only ZIP files are allowed'}, status=400)

        # 解压文件
        with zipfile.ZipFile(file.file, 'r') as zip_ref:
            zip_ref.extractall('extracted_files')

        # 返回解压成功的响应
        return response.json({'message': 'File decompressed successfully'}, status=200)
    except zipfile.BadZipFile:
        # 处理坏的ZIP文件
        return response.json({'error': 'Invalid ZIP file'}, status=400)
    except Exception as e:
        # 处理其他异常
        return response.json({'error': str(e)}, status=500)

# 运行Sanic应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, workers=1)

"""
FileDecompressionService
=======================

This is a simple Sanic application that provides a REST API for decompressing ZIP files.

API Endpoints
------------
/api/decompress (POST)
    - Decompresses a provided ZIP file and extracts its contents to the 'extracted_files' directory.

Error Handling
--------------
- If no file is provided, returns a 400 error with a message 'No file provided'.
- If the file is not a ZIP file, returns a 400 error with a message 'Only ZIP files are allowed'.
- If the ZIP file is invalid, returns a 400 error with a message 'Invalid ZIP file'.
- If any other error occurs, returns a 500 error with the error message.

Usage
-----
To use this service, send a POST request to /api/decompress with a ZIP file in the 'file' field.

Example:
curl -X POST -F 'file=@path_to_your_file.zip' http://localhost:8000/api/decompress

Note:
- The 'extracted_files' directory will be created in the same directory as this script if it doesn't already exist.
- The extracted files will be stored in this directory.
"""