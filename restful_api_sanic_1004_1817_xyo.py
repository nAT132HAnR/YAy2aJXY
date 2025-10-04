# 代码生成时间: 2025-10-04 18:17:59
import json
from sanic import Sanic, response
from sanic.exceptions import ServerError
from sanic.log import logger
from sanic.response import json as sanic_json

# 创建Sanic应用
app = Sanic('RESTful API')

# 定义全局数据存储
# 这里使用字典模拟数据库存储
users = {
    "1": {"name": "Alice", "age": 30},
    "2": {"name": "Bob", "age": 25}
}

# 获取用户列表的接口
@app.route('/users', methods=['GET'])
async def get_users(request):
    return sanic_json(users)

# 获取单个用户的接口
@app.route('/users/<user_id>', methods=['GET'])
async def get_user(request, user_id):
    user = users.get(user_id)
    if not user:
        return response.json({'error': 'User not found'}, status=404)
    return sanic_json(user)

# 创建用户的接口
@app.route('/users', methods=['POST'])
async def create_user(request):
    data = request.json
    if 'name' not in data or 'age' not in data:
        return response.json({'error': 'Missing name or age'}, status=400)
    user_id = len(users) + 1  # 简单的ID生成逻辑
    users[str(user_id)] = data
    return response.json(users[str(user_id)], status=201)

# 更新用户的接口
@app.route('/users/<user_id>', methods=['PUT'])
async def update_user(request, user_id):
    if user_id not in users:
        return response.json({'error': 'User not found'}, status=404)
    data = request.json
    user = users[user_id]
    user.update(data)
    return sanic_json(user)

# 删除用户的接口
@app.route('/users/<user_id>', methods=['DELETE'])
async def delete_user(request, user_id):
    if user_id in users:
        del users[user_id]
        return response.json({'message': 'User deleted successfully'}, status=200)
    return response.json({'error': 'User not found'}, status=404)

# 错误处理
@app.exception(ServerError)
async def handle_server_error(request, exception):
    logger.error(exception)
    return response.json({'error': 'Internal Server Error'}, status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)