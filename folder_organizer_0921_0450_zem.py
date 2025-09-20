# 代码生成时间: 2025-09-21 04:50:12
import os
import shutil
from sanic import Sanic, response
from sanic.exceptions import ServerError
from sanic.request import Request

# FolderOrganizer class to handle folder operations
class FolderOrganizer:
    def __init__(self, root_folder):
        self.root_folder = root_folder

    def move_files(self, source, target, extension=None):
        """Move files from source to target folder based on file extension"""
        if not os.path.exists(self.root_folder):
            raise FileNotFoundError(f"The root folder {self.root_folder} does not exist")

        for file_name in os.listdir(source):
            if extension and not file_name.endswith(extension):
                continue
            file_path = os.path.join(source, file_name)
            target_path = os.path.join(target, file_name)
            try:
                shutil.move(file_path, target_path)
            except Exception as e:
                raise ServerError(f"Failed to move file {file_name}: {e}")

# Sanic application
app = Sanic("FolderOrganizerApp")

@app.exception(ServerError)
async def handle_server_error(request: Request, exception: ServerError):
    "