# 代码生成时间: 2025-09-11 19:17:57
import json
from sanic import Sanic, response
from sanic.exceptions import ServerError

# 创建Sanic应用
app = Sanic('APIResponseFormatter')

# API响应格式化工具类
class ApiResponseFormatter:
    def __init__(self):
        """初始化响应格式化工具"""
        pass

    def format_response(self, data, message, status_code):
        "