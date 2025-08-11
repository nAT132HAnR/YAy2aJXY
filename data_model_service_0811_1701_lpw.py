# 代码生成时间: 2025-08-11 17:01:10
from sanic import Sanic, response
from sanic.exceptions import ServerError, NotFound
from peewee import Model, CharField, IntegerField, SqliteDatabase
from playhouse.shortcuts import model_to_dict

# 数据库初始化
db = SqliteDatabase('my_database.db')

# 定义数据模型
class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField(unique=True)
    email = CharField(unique=True)
    age = IntegerField()

# 创建表
db.create_tables([User])

# 定义API路由
app = Sanic('DataModelService')

@app.route('/users/', methods=['GET'])
async def get_users(request):
    try:
        users = User.select()
        return response.json([model_to_dict(user) for user in users])
    except Exception as e:
        raise ServerError(f"An error occurred: {e}")

@app.route('/users/<int:user_id>/', methods=['GET'])
async def get_user(request, user_id):
    try:
        user = User.get(User.id == user_id)
        return response.json(model_to_dict(user))
    except User.DoesNotExist:
        raise NotFound('User not found')
    except Exception as e:
        raise ServerError(f"An error occurred: {e}")

@app.route('/users/', methods=['POST'])
async def create_user(request):
    try:
        data = request.json
        user = User.create(username=data['username'], email=data['email'], age=data['age'])
        return response.json(model_to_dict(user), status=201)
    except Exception as e:
        raise ServerError(f"An error occurred: {e}")

@app.exception(ServerError)
async def handle_server_error(request, exception):
    return response.json({'error': str(exception)}, status=500)

@app.exception(NotFound)
async def handle_not_found(request, exception):
    return response.json({'error': str(exception)}, status=404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)