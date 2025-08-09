# 代码生成时间: 2025-08-09 14:52:16
from sanic import Sanic
from sanic.response import json, text
from sanic.exceptions import ServerError, NotFound, abort

# 初始化Sanic应用
app = Sanic(__name__)

# 错误处理器
@app.exception(NotFound)
async def not_found(request, exception):
    return text('The resource was not found', status=404)

@app.exception(ServerError)
async def server_error(request, exception):
    return text('Internal server error', status=500)

# 定义一个简单GET接口
@app.route('/api/hello', methods=['GET'])
async def hello(request):
    """
    API endpoint to return a greeting
    """
    return json({'message': 'Hello, World!'})

# 定义另一个GET接口，带参数
@app.route('/api/greet/<name>', methods=['GET'])
async def greet(request, name):
    """
    API endpoint to return a personalized greeting
    :param name: the name of the person to greet
    """
    return json({'message': f'Hello, {name}!'})

# 定义POST接口
@app.route('/api/message', methods=['POST'])
async def post_message(request):
    """
    API endpoint to receive a message and respond
    """
    data = request.json
    if not data:
        return json({'error': 'No data provided'}, status=400)
    message = data.get('message')
    if not message:
        return json({'error': 'Message is required'}, status=400)
    return json({'received': message})

if __name__ == '__main__':
    # 运行Sanic应用
    app.run(host='0.0.0.0', port=8000, debug=True)