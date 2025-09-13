# 代码生成时间: 2025-09-14 01:19:18
import asyncio
from sanic import Sanic, response
from sanic.exceptions import ServerError, NotFound
from dataclasses import dataclass, field
from typing import List
from marshmallow import Schema, fields, validate, ValidationError

# 数据模型类
@dataclass
class User:
    id: int = field(default=None)
    name: str = field(default="")
    email: str = field(default="")
    
    # 校验邮箱格式
    @validate("email")
    def validate_email(self, value):
        if "@" not in value or "." not in value:
            raise ValueError("Invalid email address")
        return value

# 创建Sanic应用
app = Sanic("DataModelService")

# 创建用户数据模型的Schema，用于序列化和反序列化
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)

# 错误处理器
@app.exception(ValidationError)
async def handle_validation_error(request, exception):
    return response.json(
        {
            "error": "Validation error",
            "messages": str(exception.messages)
        },
        status=400,
    )

@app.exception(NotFound)
async def handle_not_found(request, exception):
    return response.json(
        {"error": "Not found"},
        status=404,
    )

# 创建用户路由
@app.route("/users", methods=["POST"])
async def create_user(request):
    user_schema = UserSchema()
    try:
        # 反序列化请求体
        user_data = user_schema.load(request.json)
        # 创建User对象
        user = User(name=user_data["name"], email=user_data["email"])
        # 处理用户创建逻辑（此处省略）
        return response.json(user)
    except ValidationError as e:
        raise ServerError("Invalid data", e.messages)

# 启动Sanic应用
if __name__ == "__main__":
    with app:
        app.run(host="0.0.0.0", port=8000, debug=True)
