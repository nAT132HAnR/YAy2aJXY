# 代码生成时间: 2025-09-04 03:01:20
import json
from sanic import Sanic, response
from sanic.exceptions import ServerError
from sanic.response import json as sanic_json_response

# 定义一个JSON数据格式转换器的Sanic服务
app = Sanic('json_converter_service')

# 错误处理中间件
@app.exception(ServerError)
async def handle_server_error(request, exception):
    # 返回500错误响应
    return response.json({'error': 'Internal Server Error'}, status=500)

# 路由：用于处理POST请求，接收JSON数据并转换
@app.route('/api/convert', methods=['POST'])
async def convert_json(request):
    # 获取请求体中的JSON数据
    try:
        data = request.json
    except json.JSONDecodeError:
        # 如果JSON数据格式错误，返回400错误响应
        return response.json({'error': 'Invalid JSON format'}, status=400)
    
    # 将接收到的JSON数据转换为字符串格式
    converted_data = json.dumps(data)
    
    # 返回转换后的JSON字符串
    return sanic_json_response({'converted_data': converted_data})

# 运行Sanic服务
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)