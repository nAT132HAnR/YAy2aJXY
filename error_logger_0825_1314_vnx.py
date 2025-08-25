# 代码生成时间: 2025-08-25 13:14:36
import asyncio
from sanic import Sanic, response
from sanic.exceptions import ServerError
from sanic.request import Request
from sanic.response import json
import logging

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 创建Sanic应用
app = Sanic("ErrorLogger")

# 定义错误日志存储列表
error_logs = []

# 定义错误日志收集器的路由
@app.route("/log_error", methods=["POST"])
async def log_error(request: Request):
    # 从请求体中获取错误信息
    error_data = request.json
    
    # 检查错误信息是否有效
    if not error_data or 'error_message' not in error_data:
        return response.json({'error': 'Invalid error data'}, status=400)
    
    # 将错误信息添加到日志列表
    error_logs.append(error_data)
    
    # 日志记录错误信息
    logging.error(f"New error logged: {error_data['error_message']}")
    
    # 返回成功响应
    return response.json({'message': 'Error logged successfully'}, status=200)

# 定义获取所有错误日志的路由
@app.route("/get_errors", methods=["GET"])
async def get_errors(request: Request):
    # 返回所有错误日志
    return response.json({'errors': error_logs}, status=200)

# 定义错误处理器
@app.exception
def handle_request_exception(request: Request, exception: Exception):
    # 捕获并记录所有未处理的异常
    logging.error(f"Unhandled exception: {exception}")
    
    # 将异常信息添加到错误日志列表
    error_logs.append({'error_message': str(exception)})
    
    # 返回错误响应
    return response.json({'error': 'An unexpected error occurred'}, status=500)

# 运行Sanic应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)