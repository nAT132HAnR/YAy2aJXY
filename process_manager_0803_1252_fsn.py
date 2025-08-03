# 代码生成时间: 2025-08-03 12:52:50
import asyncio
from sanic import Sanic, response
from sanic.exceptions import ServerError
from sanic.request import Request
from sanic.response import HTTPResponse
import subprocess
import psutil
import sys
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Sanic("ProcessManager")

\@app.exception(ServerError)
async def handle_exception(request: Request, exception: ServerError):
    """全局异常处理"""
    return response.json({"error": str(exception)}, status=500)

@app.route("/start/<process_name:path>", methods=["POST"])
async def start_process(request: Request, process_name: str):
    """启动一个新的进程"""
    try:
        process = subprocess.Popen([process_name])
        return response.json({"message": f"Process {process_name} started successfully.", "pid": process.pid})
    except Exception as e:
        logger.error(f"Failed to start process {process_name}: {e}")
        return response.json({"error": f"Failed to start process {process_name}: {e}"}, status=500)

@app.route("/stop/<process_name:path>", methods=["POST"])
async def stop_process(request: Request, process_name: str):
    """停止一个进程"""
    try:
        # 寻找所有匹配的进程
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == process_name:
                proc.kill()
                proc.wait()
                return response.json({"message": f"Process {process_name} stopped successfully."})
        return response.json({"error": f"No running process found for {process_name}."}, status=404)
    except Exception as e:
        logger.error(f"Failed to stop process {process_name}: {e}")
        return response.json({"error": f"Failed to stop process {process_name}: {e}"}, status=500)

@app.route("/list", methods=["GET"])
async def list_processes(request: Request):
    """列出所有进程"""
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'status']):
            processes.append({
                "pid": proc.info['pid'],
                "name": proc.info['name'],
                "status": proc.info['status']
            })
        return response.json(processes)
    except Exception as e:
        logger.error(f"Failed to list processes: {e}")
        return response.json({"error": f"Failed to list processes: {e}"}, status=500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, auto_reload=False)