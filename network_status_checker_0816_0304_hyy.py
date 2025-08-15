# 代码生成时间: 2025-08-16 03:04:06
import asyncio
from sanic import Sanic, response
from sanic.exceptions import ServerError
from aiohttp import ClientSession
from urllib.parse import urlparse

# 创建一个Sanic应用
app = Sanic("NetworkStatusChecker")

# 异步检查网络连接状态的函数
async def check_connection(url: str) -> bool:
    """
    检查给定URL的网络连接状态。
    
    :param url: 需要检查的URL
    :return: 如果连接成功返回True，否则返回False
    """
    try:
        async with ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return True
    except Exception as e:
        # 遇到任何异常，返回False
        print(f"An error occurred: {e}")
        return False

# Sanic路由，用于检查网络连接状态
@app.route("/check", methods=["GET"])
async def check_status(request):
    """
    处理HTTP GET请求，检查网络连接状态。
    
    :param request: HTTP请求对象
    :return: 包含网络连接状态的JSON响应
    """
    url = request.args.get("url")
    if not url:
        # 如果URL参数不存在，返回错误响应
        return response.json({
            "error": "URL parameter is missing"
        }, status=400)
    
    # 解析URL，检查是否有效
    parsed_url = urlparse(url)
    if not all([parsed_url.scheme, parsed_url.netloc]):
        return response.json({
            "error": "Invalid URL"
        }, status=400)
        
    # 检查网络连接状态
    connection_status = await check_connection(url)
    
    # 返回结果
    return response.json({
        "url": url,
        "status": "connected" if connection_status else "disconnected"
    })

# 捕获未处理的异常
@app.exception
async def handle_request_exception(request, exception):
    """
    处理Sanic应用中的所有未处理异常。
    
    :param request: HTTP请求对象
    :param exception: 异常对象
    :return: 错误信息的JSON响应
    """
    if isinstance(exception, ServerError):
        return response.json({
            "error": f"Internal Server Error: {exception}"
        }, status=500)
    else:
        return response.json({
            "error": "An unexpected error occurred"
        }, status=500)

# 运行Sanic应用
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)