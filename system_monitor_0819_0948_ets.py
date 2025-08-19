# 代码生成时间: 2025-08-19 09:48:21
import psutil
from sanic import Sanic, response
from sanic.exceptions import ServerError

# 定义一个类来封装系统性能监控的功能
class SystemMonitor:
    def __init__(self):
        pass

    # 获取CPU使用率
    def get_cpu_usage(self):
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            return {'cpu_usage': cpu_usage}
        except Exception as e:
            raise ServerError("Failed to get CPU usage", e)

    # 获取内存使用情况
    def get_memory_usage(self):
        try:
            memory = psutil.virtual_memory()
            return {'memory_usage': memory.percent}
        except Exception as e:
            raise ServerError("Failed to get memory usage", e)

    # 获取磁盘使用情况
    def get_disk_usage(self):
        try:
            disk_usage = psutil.disk_usage('/')
            return {'disk_usage': disk_usage.percent}
        except Exception as e:
            raise ServerError("Failed to get disk usage", e)


# 创建Sanic应用
app = Sanic("SystemMonitor")

# 定义路由处理函数，获取系统性能监控数据
@app.route("/monitor", methods=["GET"])
async def monitor(request):
    try:
        monitor_data = SystemMonitor()
        cpu_data = monitor_data.get_cpu_usage()
        memory_data = monitor_data.get_memory_usage()
        disk_data = monitor_data.get_disk_usage()
        # 将数据合并到一个字典中
        data = {**cpu_data, **memory_data, **disk_data}
        return response.json(data)
    except ServerError as e:
        return response.json({"error": str(e)})
    except Exception as e:
        return response.json({"error": "An unexpected error occurred"}, status=500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)