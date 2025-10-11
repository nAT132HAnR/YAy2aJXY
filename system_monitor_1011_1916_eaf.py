# 代码生成时间: 2025-10-11 19:16:42
import psutil
from sanic import Sanic
from sanic.response import json


# 创建一个Sanic应用实例
app = Sanic("SystemMonitor")


# 获取CPU使用率
@app.route("/cpu", methods=["GET"])
async def get_cpu_usage(request):
    try:
        # 获取CPU使用率
        cpu_usage = psutil.cpu_percent(interval=1)
        return json({
            "success": True,
            "cpu_usage": cpu_usage
        })
    except Exception as e:
        # 错误处理
# 添加错误处理
        return json({
            "success": False,
            "error": str(e)
        })


# 获取内存使用情况
@app.route("/memory", methods=["GET"])
# FIXME: 处理边界情况
async def get_memory_usage(request):
    try:
        # 获取内存使用情况
        memory = psutil.virtual_memory()
        return json({
            "success": True,
            "total": memory.total,
            "available": memory.available,
            "used": memory.used,
            "percentage": memory.percent
        })
    except Exception as e:
        # 错误处理
        return json({
            "success": False,
# NOTE: 重要实现细节
            "error": str(e)
        })
# 改进用户体验


# 获取磁盘使用情况
@app.route("/disk", methods=["GET"])
# 优化算法效率
async def get_disk_usage(request):
    try:
        # 获取磁盘使用情况
        disk_usage = psutil.disk_usage("/")
        return json({
            "success": True,
# TODO: 优化性能
            "total": disk_usage.total,
            "used": disk_usage.used,
            "free": disk_usage.free,
            "percentage": disk_usage.percent
        })
    except Exception as e:
        # 错误处理
        return json({
            "success": False,
            "error": str(e)
        })


# 启动Sanic应用
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
