# 代码生成时间: 2025-09-14 17:21:40
# log_parser.py
# 这是一个使用Python和Sanic框架创建的日志文件解析工具

import sanic
from sanic.response import json
import logging
from datetime import datetime
import re

# 定义日志解析器类
class LogParser:
    # 初始化解析器，设置日志文件路径
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path

    # 解析日志文件
    def parse_log_file(self):
        try:
            with open(self.log_file_path, 'r') as file:
                logs = file.readlines()
            return self.parse_logs(logs)
        except FileNotFoundError:
            return {'error': '日志文件未找到'}
        except Exception as e:
            return {'error': str(e)}

    # 解析日志行
    def parse_logs(self, logs):
        parsed_logs = []
        for log in logs:
            try:
                # 使用正则表达式解析日志行
                match = re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - (.*)", log)
                if match:
                    # 将时间字符串格式化为datetime对象
                    timestamp = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S,%f')
                    level = match.group(2)
                    parsed_logs.append({'timestamp': timestamp, 'level': level})
            except Exception as e:
                logging.error(f'解析日志时出错: {e}')
        return parsed_logs

# 创建Sanic应用
app = sanic.Sanic('LogParserApp')

# 定义路由处理函数，用于解析日志文件
@app.route('/api/parse', methods=['POST'])
async def parse_log(request):
    log_file_path = request.json.get('log_file_path')
    if not log_file_path:
        return json({'error': '缺少日志文件路径参数'}, status=400)

    parser = LogParser(log_file_path)
    parsed_logs = parser.parse_log_file()
    return json(parsed_logs)

# 运行Sanic应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)