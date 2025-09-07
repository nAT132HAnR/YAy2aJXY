# 代码生成时间: 2025-09-07 11:26:59
import psutil
from sanic import Sanic, response

# 初始化Sanic应用
app = Sanic("SystemMonitor")

# 系统性能监控工具的路由
@app.route("/monitor", methods=["GET"])
async def monitor(request):
    try:
        # 收集CPU使用率
        cpu_usage = psutil.cpu_percent()
        
        # 收集内存使用信息
        memory = psutil.virtual_memory()
        
        # 收集磁盘使用信息
        disk = psutil.disk_usage('/')
        
        # 构建响应数据
        data = {
            "cpu_usage": cpu_usage,
            "memory": {
                "total": memory.total,
                "available": memory.available,
                "used": memory.used,
                "percentage": memory.percent
            },
            "disk": {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percentage": disk.percent
            }
        }
        
        # 返回JSON格式的响应
        return response.json(data)
    except Exception as e:
        # 处理异常并返回错误信息
        return response.json({"error": str(e)})

# 运行Sanic应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)