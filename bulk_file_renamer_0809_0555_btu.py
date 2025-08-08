# 代码生成时间: 2025-08-09 05:55:47
import os
import sanic
from sanic.response import json, text
from sanic.exceptions import ServerError
from sanic.log import logger

# 定义批量文件重命名工具的函数
def bulk_rename(directory, rename_pattern):
    """
    批量重命名指定目录下的文件，按照rename_pattern进行重命名。
    :param directory: 要重命名文件的目录
    :param rename_pattern: 重命名规则，例如：'{index}_{original_name}.ext'
    :return: 重命名结果
    """
    renamed_files = []
    index = 0
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            new_name = rename_pattern.format(index=index, original_name=filename)
            try:
                os.rename(os.path.join(directory, filename), os.path.join(directory, new_name))
                renamed_files.append((filename, new_name))
            except Exception as e:
                logger.error(f'Failed to rename {filename} to {new_name}. Error: {str(e)}')
    return renamed_files

# 创建Sanic应用
app = sanic.Sanic('BulkFileRenamer')

# 添加路由处理POST请求
@app.route('/api/rename', methods=['POST'])
async def rename_files(request):
    """
    API端点用于接收批量重命名请求。
    :param request: 请求对象
    :return: 重命名结果
    """
    try:
        data = request.json
        if 'directory' not in data or 'rename_pattern' not in data:
            raise ServerError('Missing required parameters: directory or rename_pattern')
        directory = data['directory']
        rename_pattern = data['rename_pattern']
        result = bulk_rename(directory, rename_pattern)
        return json({'status': 'success', 'data': result})
    except Exception as e:
        logger.error(f'Error renaming files: {str(e)}')
        return text(str(e), status=500)

# 运行应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, workers=1)