# 代码生成时间: 2025-08-27 23:02:52
import asyncio
from sanic import Sanic, response
from sanic.exceptions import ServerError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.executors.asyncio import AsyncIOExecutor


# 初始化定时任务调度器
scheduler = AsyncIOScheduler(AsyncIOExecutor())
scheduler.start()


# 创建Sanic应用
app = Sanic(__name__)


# 定时任务函数
async def scheduled_task():
    try:
        # 这里可以定义具体的定时任务逻辑
        print("Scheduled task executed.")
    except Exception as e:
        # 处理可能发生的错误
        print(f"Error occurred during scheduled task: {e}")


# 设置定时任务，每天的00:00执行
scheduler.add_job(scheduled_task, CronTrigger(hour=0, minute=0))


# 创建Sanic路由，用于检查定时任务调度器的状态
@app.route('/ping', methods=['GET'])
async def ping(request):
    try:
        return response.json({'message': 'PONG', 'scheduler_state': scheduler.state})
    except Exception as e:
        # 将异常信息包装成500错误响应
        raise ServerError("Server encountered an error.", status_code=500)


if __name__ == '__main__':
    # 启动Sanic服务器
    app.run(host='0.0.0.0', port=8000)
