# 代码生成时间: 2025-08-30 21:59:29
import asyncio
from sanic import Sanic, response
from sanic.exceptions import ServerError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger


# 定义定时任务调度器类
class ScheduledTaskScheduler:
    def __init__(self, app: Sanic):
        self.app = app
        self.scheduler = AsyncIOScheduler()
        self.scheduler.start()

    def add_task(self, func, interval):
        """添加定时任务"""
        self.scheduler.add_job(func, trigger=IntervalTrigger(seconds=interval), id=func.__name__)

    def shutdown(self):
        """关闭调度器"""
        self.scheduler.shutdown()


# 创建Sanic应用
app = Sanic('ScheduledTaskSchedulerApp')

# 创建定时任务调度器实例
scheduler = ScheduledTaskScheduler(app)

# 定义定时执行的函数
async def scheduled_task():
    """这是一个定时执行的任务函数"""
    print("Scheduled task executed at: ", datetime.now())
    try:
        # 这里可以放置定时任务需要执行的代码
        pass
    except Exception as e:
        # 错误处理
        print(f"Error in scheduled_task: {e}")

# 添加定时任务
scheduler.add_task(scheduled_task, 10)

# 定义Sanic路由
@app.route('/')
async def index(request):
    """首页路由"""
    return response.json({'message': 'Scheduled task scheduler is running...'})

# 错误处理中间件
@app.exception(ServerError)
async def handle_server_error(request, exception):
    """处理服务器错误"""
    return response.json({'error': str(exception)}, status=500)

# 运行Sanic应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)