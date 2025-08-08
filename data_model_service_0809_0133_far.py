# 代码生成时间: 2025-08-09 01:33:20
import sanic
from sanic import response
from sanic.exceptions import ServerError, abort
from peewee import Model, CharField, IntegerField, SqliteDatabase


# 数据库初始化
db = SqliteDatabase('data_model.db')


# 定义数据模型
class BaseModel(Model):
    """数据库基础模型"""
    class Meta:
        database = db


class User(BaseModel):
    """用户模型"""
    username = CharField(unique=True)
    age = IntegerField()

# 创建表
db.create_tables([User], safe=True)


# 定义Sanic应用
app = sanic.Sanic(__name__)


@app.exception(ServerError)
async def handle_server_error(request, exception):
    """错误处理"""
    return response.json({'error': str(exception)}, status=500)


@app.route('/users', methods=['GET'])
async def get_users(request):
    """获取所有用户"""
    try:
        users = User.select()
        return response.json([{'username': user.username, 'age': user.age} for user in users])
    except Exception as e:
        abort(500, 'Internal Server Error')

@app.route('/users', methods=['POST'])
async def add_user(request):
    """添加新用户"""
    try:
        data = request.json
        username = data.get('username')
        age = data.get('age')

        if not username or not age:
            abort(400, 'Missing required fields')

        user, _ = User.get_or_create(username=username, age=age)
        return response.json({'username': user.username, 'age': user.age}, status=201)
    except Exception as e:
        abort(500, 'Internal Server Error')


if __name__ == '__main__':
    """运行Sanic应用"""
    app.run(host='0.0.0.0', port=8000, debug=True)