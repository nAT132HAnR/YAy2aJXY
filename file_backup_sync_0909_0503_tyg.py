# 代码生成时间: 2025-09-09 05:03:06
import os
import shutil
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import HTTPResponse
from sanic.exceptions import ServerError
from sanic_cors import CORS

# 配置Sanic应用
app = Sanic("FileBackupSync")

# 启用CORS
CORS(app)

# 配置源目录和备份目录
SOURCE_DIR = "/path/to/source"
BACKUP_DIR = "/path/to/backup"

# 同步文件
def sync_files(src, dst, ignore=None):
    """
    同步文件从源目录到目标目录。

    :param src: 源目录路径
    :param dst: 目标目录路径
    :param ignore: 忽略文件列表
    """
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            sync_files(s, d, ignore)
        else:
            if ignore is not None and item in ignore:
                continue
            if not os.path.exists(d):
                shutil.copy2(s, d)
            else:
                file_src_stat = os.stat(s)
                file_dst_stat = os.stat(d)
                if file_src_stat.st_mtime - file_dst_stat.st_mtime > 1:
                    shutil.copy2(s, d)

# 定义备份文件的路由
@app.route("/backup", methods=["GET", "POST"])
async def backup_file(request: Request):
    try:
        # 同步文件备份
        sync_files(SOURCE_DIR, BACKUP_DIR)
        return response.json({"message": "Files backed up successfully"})
    except Exception as e:
        # 错误处理
        raise ServerError("Failed to backup files", e)

# 启动Sanic应用
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)