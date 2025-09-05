# 代码生成时间: 2025-09-05 23:22:08
import asyncio
import subprocess
from sanic import Sanic, response
from sanic.request import Request
from sanic.exceptions import ServerError
from sanic.response import json

# Define the ProcessManager class to handle process-related operations
class ProcessManager:
    def __init__(self):
        self.processes = {}

    # Start a new process
    async def start_process(self, name, command):
        try:
            # Create a subprocess and store it in the dictionary
            self.processes[name] = subprocess.Popen(command, shell=True)
            return {"message": f"Process {name} started successfully"}
        except Exception as e:
            raise ServerError(f"Failed to start process {name}: {str(e)}")

    # Stop a process by name
    async def stop_process(self, name):
        try:
            # Check if the process exists and stop it
            if name in self.processes:
                self.processes[name].terminate()
                self.processes[name].wait()
                del self.processes[name]
                return {"message": f"Process {name} stopped successfully"}
            else:
                raise ServerError(f"Process {name} not found")
        except Exception as e:
            raise ServerError(f"Failed to stop process {name}: {str(e)}")

    # Get the status of a process by name
    async def get_process_status(self, name):
        try:
            # Check if the process exists and return its status
            if name in self.processes:
                return {"name": name, "status": "running" if self.processes[name].poll() is None else "stopped"}
            else:
                raise ServerError(f"Process {name} not found")
        except Exception as e:
            raise ServerError(f"Failed to get status of process {name}: {str(e)}")

# Create a Sanic application
app = Sanic("ProcessManager")
process_manager = ProcessManager()

# Define routes for the process manager
@app.route("/start", methods=["POST"])
async def start_process(request: Request):
    name = request.json.get("name")
    command = request.json.get("command")
    if not name or not command:
        return response.json({
            "error": "Missing name or command in request"
        }, status=400)
    result = await process_manager.start_process(name, command)
    return response.json(result)

@app.route("/stop", methods=["POST"])
async def stop_process(request: Request):
    name = request.json.get("name")
    if not name:
        return response.json({
            "error": "Missing name in request"
        }, status=400)
    result = await process_manager.stop_process(name)
    return response.json(result)

@app.route("/status", methods=["POST"])
async def get_process_status(request: Request):
    name = request.json.get("name")
    if not name:
        return response.json({
            "error": "Missing name in request"
        }, status=400)
    result = await process_manager.get_process_status(name)
    return response.json(result)

# Run the Sanic application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)