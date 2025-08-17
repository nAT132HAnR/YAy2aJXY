# 代码生成时间: 2025-08-17 13:46:07
import aiohttp
from sanic import Sanic, response
from sanic.exceptions import ServerError
from sanic.request import Request
from sanic.response import json as sanic_json

# 创建Sanic应用
app = Sanic('WebContentScraper')

# 异步请求会话
session = aiohttp.ClientSession()

# 定义路由以抓取网页内容
@app.route('/scrape', methods=['GET'])
async def scrape(request: Request):
    # 获取URL参数
    url = request.args.get('url')
    if not url:
        # 如果参数不存在，返回错误信息
        return sanic_json({'error': 'URL parameter is missing'}, status=400)

    try:
        # 使用aiohttp获取网页内容
        async with session.get(url) as response:
            # 检查HTTP响应状态
            if response.status == 200:
                # 获取网页内容
                content = await response.text()
                # 返回网页内容
                return sanic_json({'status': 'success', 'content': content})
            else:
                # 返回错误状态
                return sanic_json({'status': 'failed', 'message': 'Failed to fetch content'}, status=response.status)
    except Exception as e:
        # 处理异常，返回错误信息
        return sanic_json({'status': 'error', 'message': str(e)}, status=500)
    finally:
        # 确保会话关闭
        await session.close()

# 定义异常处理器
@app.exception
def handle_exception(request, exception):
    # 对于ServerError异常，返回500状态码
    if isinstance(exception, ServerError):
        return response.json({'error': str(exception)}, status=500)
    # 对于其他异常，返回默认的错误信息
    return response.json({'error': 'An unexpected error occurred'}, status=500)

# 运行Sanic应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, auto_reload=False)