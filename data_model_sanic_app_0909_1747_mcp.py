# 代码生成时间: 2025-09-09 17:47:38
import sanic
from sanic import response
from sanic.exceptions import ServerError, NotFound, abort
from peewee import Model, SqliteDatabase, IntegerField, CharField
from playhouse.shortcuts import model_to_dict
from sanic.log import logger

# 数据库配置
DATABASE = SqliteDatabase('sanic_db.sqlite3')

# 定义数据模型
class BaseModel(Model):
    class Meta:
        database = DATABASE

class User(BaseModel):
    id = IntegerField(primary_key=True)
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    created_at = IntegerField(default=int)
    updated_at = IntegerField(default=int)

# 应用配置
app = sanic.Sanic('DataModelSanicApp')

# 启动前初始化数据库
@app.listener('before_server_start')
async def setup_db(app, loop):
    try:
        DATABASE.create_tables([User], safe=True)
    except Exception as e:
        logger.error(f'Database setup error: {e}')
        raise ServerError('Database setup failed')

# 用户创建接口
@app.route('/user', methods=['POST'])
async def create_user(request):
    data = request.json
    try:
        user = User.create(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        return response.json(model_to_dict(user))
    except Exception as e:
        logger.error(f'Failed to create user: {e}')
        abort(500, 'Failed to create user')

# 用户获取接口
@app.route('/user/<int:user_id>', methods=['GET'])
async def get_user(request, user_id):
    try:
        user = User.get(User.id == user_id)
        return response.json(model_to_dict(user))
    except User.DoesNotExist:
        abort(404, 'User not found')
    except Exception as e:
        logger.error(f'Failed to get user: {e}')
        abort(500, 'Failed to get user')

# 运行应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)