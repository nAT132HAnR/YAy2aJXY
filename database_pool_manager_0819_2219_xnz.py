# 代码生成时间: 2025-08-19 22:19:56
import asyncio
import aiomysql
from sanic import Sanic, response
from sanic.exceptions import ServerError
from sanic.response import json
from tenacity import retry, stop_after_attempt, wait_fixed

# 全局配置字典
config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'your_username',
    'password': 'your_password',
    'db': 'your_database',
    'charset': 'utf8mb4',
    'cursorclass': dict,  # 确保返回字典类型的结果
}

# 初始化数据库连接池
pool = None

# 重试装饰器
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def create_pool(loop):  # 使用重试机制创建连接池
    global pool
    pool = aiomysql.create_pool(
        host=config['host'],
        port=config['port'],
        user=config['user'],
        password=config['password'],
        db=config['db'],
        charset=config['charset'],
        cursorclass=config['cursorclass'],
        loop=loop,
    )

# 创建Sanic实例
app = Sanic(__name__)

@app.listener('after_server_start')
async def setup_db(app, loop):  # 服务器启动后创建数据库连接池
    create_pool(loop)

@app.listener('after_server_stop')
async def close_db(app, loop):  # 服务器停止时关闭数据库连接池
    global pool
    if pool:  # 确保连接池已创建
        await pool.close()
        await pool.wait_closed()
        pool = None

@app.exception(ServerError)
async def handle_server_error(request, exception):  # 处理服务器异常
    return response.json({'error': 'Internal Server Error'}, status=500)

@app.route('/test')
async def test_db(request):  # 测试数据库连接的路由
    global pool
    if not pool:  # 如果连接池未创建则返回错误
        return json({'error': 'Database pool not created'}, status=500)

    async with pool.acquire() as conn:  # 从连接池获取连接
        async with conn.cursor() as cursor:  # 创建游标
            await cursor.execute('SELECT 1')  # 执行测试查询
            result = await cursor.fetchone()  # 获取查询结果
            if result:  # 如果查询成功
                return json({'message': 'Database connection is working'})
            else:  # 如果查询失败
                return json({'error': 'Database query failed'}, status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, workers=2)  # 启动Sanic服务器