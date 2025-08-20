# 代码生成时间: 2025-08-20 22:05:50
import logging
from sanic import Sanic, response
from sanic.exceptions import ServerError, ServerError914RequestURITooLarge
from sanic.request import Request

# 设置日志配置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('error_collector')

# 初始化Sanic应用
app = Sanic('error_collector_service')

# 错误日志收集器
@app.exception(ServerError914RequestURITooLarge)
async def handle_uri_too_large(request: Request, exception: ServerError914RequestURITooLarge):
    """处理请求URI过大的错误"""
    logger.error(f'Request URI too large: {request.uri}')
    return response.json({'error': 'Request URI too large'}, status=414)

@app.exception(ServerError)
async def handle_server_error(request: Request, exception: ServerError):
    """处理服务器错误"""
    logger.error(f'Server error: {exception}')
    return response.json({'error': 'A server error occurred'}, status=500)

@app.route('/errors', methods=['POST'])
async def collect_errors(request: Request):
    """收集客户端发送的错误日志"""
    try:
        error_data = request.json
        logger.error(f'Error collected: {error_data}')
        return response.json({'message': 'Error collected successfully'})
    except Exception as e:
        logger.error(f'Error while collecting error: {e}')
        return response.json({'error': 'Failed to collect error'}, status=400)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)