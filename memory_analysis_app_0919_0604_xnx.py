# 代码生成时间: 2025-09-19 06:04:09
import psutil
from sanic import Sanic, response
from sanic.response import json as sanic_json


# 定义一个Sanic蓝图
app = Sanic("MemoryAnalysisApp")


@app.route("/", methods=["GET"])
async def root(request):
    # 返回欢迎信息
    return response.text("Welcome to Memory Analysis API")


@app.route("/memory", methods=["GET"])
async def memory_usage(request):
    """
    Endpoint to get memory usage statistics.
    
    Fetches memory usage data and returns the information.
    
    Returns:
        A JSON response containing memory usage statistics.
    """
    try:
        # 获取内存使用情况
        memory = psutil.virtual_memory()
        # 返回内存使用信息
        return sanic_json({
            "total": memory.total,
            "available": memory.available,
            "used": memory.used,
            "free": memory.free,
            "percent": memory.percent,
        })
    except Exception as e:
        # 错误处理
        return sanic_json({"error": str(e)}), 500


if __name__ == "__main__":
    # 运行Sanic应用
    app.run(host="0.0.0.0", port=8000, debug=True)