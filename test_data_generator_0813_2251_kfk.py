# 代码生成时间: 2025-08-13 22:51:26
import json
from sanic import Sanic, response
from sanic.exceptions import ServerError, NotFound, abort
from faker import Faker
from random import randint
from string import ascii_lowercase, digits

# 初始化 Faker 生成器
fake = Faker()

# 创建 Sanic 应用
app = Sanic("Test Data Generator")

# 路由：生成测试数据
@app.route("/generate", methods=["GET"])
async def generate_test_data(request):
    # 检查请求参数
    if 'type' not in request.args:
        abort(400, 'Missing required query parameter: type')

    # 根据请求类型生成测试数据
    data_type = request.args.get('type')
    if data_type == 'user':
        return response.json(await generate_user_data())
    elif data_type == 'product':
        return response.json(await generate_product_data())
    else:
        abort(400, 'Invalid type parameter')

# 异步生成用户数据
async def generate_user_data():
    # 随机生成用户信息
    user_data = {
        "id": randint(1000, 9999),
        "name": fake.name(),
        "email": fake.email(),
        "address": fake.address(),
        "phone": fake.phone_number()
    }
    return user_data

# 异步生成产品数据
async def generate_product_data():
    # 随机生成产品信息
    product_data = {
        "id": randint(1000, 9999),
        "name": fake.word() + ' ' + fake.word(),
        "description": fake.sentence(),
        "price": fake.random_number(digits=3),
        "stock": randint(1, 100)
    }
    return product_data

# 错误处理
@app.exception
async def handle_request_exception(request, exception):
    if isinstance(exception, ServerError):
        return response.json(
            {
                "error": "Internal Server Error",
                "message": str(exception)
            },
            status=500
        )
    elif isinstance(exception, NotFound):
        return response.json(
            {
                "error": "Not Found",
                "message": str(exception)
            },
            status=404
        )
    else:
        return response.json(
            {
                "error": "Bad Request",
                "message": "Unknown error occurred"
            },
            status=400
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, workers=1)