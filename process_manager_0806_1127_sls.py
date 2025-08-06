# 代码生成时间: 2025-08-06 11:27:06
import asyncio
from sanic import Sanic, response
from sanic.exceptions import ServerError
from multiprocessing import Process, active_children
from psutil import Popen, Process as PsProcess


# 创建Sanic应用实例
app = Sanic("Process Manager")


# 启动进程
async def start_process(proc_name, cmd):
    """
    启动一个新进程
    :param proc_name: 进程名称
    :param cmd: 执行命令
    :return: 进程ID
    """
    try:
        process = Popen(cmd, shell=True)
        return process.pid
    except Exception as e:
        raise ServerError("Failed to start process", str(e))



# 终止进程
async def stop_process(pid):
    """
    终止一个进程
    :param pid: 进程ID
    :return: None
    """
    try:
        process = PsProcess(pid)
        if process.is_running():
            process.terminate()
            process.wait()
        else:
            raise ServerError("Process not running or not found")
    except Exception as e:
        raise ServerError("Failed to stop process", str(e))



# 获取所有子进程信息
async def get_child_processes():
    """
    获取所有子进程信息
    :return: 子进程列表
    """
    child_processes = []
    children = active_children()
    for child in children:
        child_processes.append({
            "name": child.name,
            "pid": child.pid,
            "is_alive": child.is_alive()
        })
    return child_processes



# 定义路由
@app.route("/start", methods=["POST"])
async def start_process_route(request):
    """
    处理启动进程请求
    """
    data = request.json
    proc_name = data.get("proc_name")
    cmd = data.get("cmd\)
    if not proc_name or not cmd:
        return response.json("Invalid request", status=400)
    try:
        pid = await start_process(proc_name, cmd)
        return response.json({"pid": pid})
    except ServerError as e:
        return response.json(str(e), status=500)


@app.route("/stop", methods=["POST"])
async def stop_process_route(request):
    """
    处理终止进程请求
    """
    data = request.json
    pid = data.get("pid")
    if not pid:
        return response.json("Invalid request", status=400)
    try:
        await stop_process(pid)
        return response.json({"message": "Process stopped successfully"})
    except ServerError as e:
        return response.json(str(e), status=500)


@app.route("/children", methods=["GET"])
async def get_child_processes_route(request):
    """
    处理获取子进程信息请求
    """
    try:
        child_processes = await get_child_processes()
        return response.json(child_processes)
    except ServerError as e:
        return response.json(str(e), status=500)



# 运行Sanic应用
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, workers=1)