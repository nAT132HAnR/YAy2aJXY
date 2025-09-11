# 代码生成时间: 2025-09-11 14:51:29
import os
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import json

# 创建Sanic应用
app = Sanic("BatchRenameTool")

# 定义批量重命名的函数
def batch_rename(folder_path, rename_pattern):
    """批量重命名文件夹中的文件
    
    :param folder_path: 文件夹路径
    :param rename_pattern: 重命名模式，例如：'file_{index}.txt'"