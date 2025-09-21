# 代码生成时间: 2025-09-21 17:43:45
import psutil
import sanic
from sanic.response import json

# Define the Sanic app
app = sanic.Sanic("SystemMonitor")

# Endpoint to get CPU usage
@app.route("/cpu", methods=["GET"])
async def get_cpu_usage(request):
    try:
        # Get CPU usage percentage
        cpu_usage = psutil.cpu_percent(interval=1)
        return json({
            "status": "success",
            "cpu_usage": cpu_usage
        })
    except Exception as e:
        # Handle any exceptions and return an error message
        return json({
            "status": "error",
            "message": str(e)
        }, status=500)

# Endpoint to get memory usage
@app.route("/memory", methods=["GET"])
async def get_memory_usage(request):
    try:
        # Get memory usage details
        memory = psutil.virtual_memory()
        memory_usage = {
            "total": memory.total,
            "available": memory.available,
            "used": memory.used,
            "percentage": memory.percent
        }
        return json({
            "status": "success",
            "memory_usage": memory_usage
        })
    except Exception as e:
        # Handle any exceptions and return an error message
        return json({
            "status": "error",
            "message": str(e)
        }, status=500)

# Endpoint to get disk usage
@app.route("/disk", methods=["GET"])
async def get_disk_usage(request):
    try:
        # Get disk usage details
        disk_usage = psutil.disk_usage('/')
        disk_usage_info = {
            "total": disk_usage.total,
            "used": disk_usage.used,
            "free": disk_usage.free,
            "percentage": disk_usage.percent
        }
        return json({
            "status": "success",
            "disk_usage": disk_usage_info
        })
    except Exception as e:
        # Handle any exceptions and return an error message
        return json({
            "status": "error",
            "message": str(e)
        }, status=500)

if __name__ == "__main__":
    # Run the Sanic app
    app.run(host="0.0.0.0", port=8000, debug=True)