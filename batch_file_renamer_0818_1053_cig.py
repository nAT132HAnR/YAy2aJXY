# 代码生成时间: 2025-08-18 10:53:52
import os
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import json
from sanic.exceptions import ServerError, NotFound

# 定义批量文件重命名的类
class BatchFileRenamer:
    def __init__(self, directory):
        self.directory = directory

    def rename_files(self, new_names_list):
        """
        批量重命名文件
        :param new_names_list: 包含新文件名的列表
        :return: 重命名结果的列表
        """
        results = []
        for i, filename in enumerate(os.listdir(self.directory)):
            if i >= len(new_names_list):
                break
            new_name = new_names_list[i]
            try:
                os.rename(os.path.join(self.directory, filename),
                          os.path.join(self.directory, new_name))
                results.append(f"Renamed {filename} to {new_name}")
            except Exception as e:
                results.append(f"Failed to rename {filename}: {e}")
        return results

# 初始化Sanic应用
app = Sanic(__name__)

# 定义端点处理批量重命名文件的请求
@app.route('/api/rename', methods=['POST'])
async def rename_files(request: Request):
    try:
        data = request.json
        directory = data.get('directory')
        new_names_list = data.get('new_names')
        if not directory or not new_names_list:
            raise ValueError("Directory and new names list are required")
        renamer = BatchFileRenamer(directory)
        results = renamer.rename_files(new_names_list)
        return response.json(results)
    except Exception as e:
        return response.json(str(e), status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)