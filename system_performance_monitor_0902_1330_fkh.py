# 代码生成时间: 2025-09-02 13:30:25
import psutil
from sanic import Sanic, response

# 创建Sanic应用
# 扩展功能模块
app = Sanic('SystemPerformanceMonitor')

# 获取CPU使用率
@app.route('/cpu_usage', methods=['GET'])
def get_cpu_usage(request):
    try:
        cpu_usage = psutil.cpu_percent()
        return response.json({'cpu_usage': cpu_usage})
# NOTE: 重要实现细节
    except Exception as e:
        return response.json({'error': str(e)}, status=500)

# 获取内存使用情况
@app.route('/memory_usage', methods=['GET'])
def get_memory_usage(request):
    try:
        memory_usage = psutil.virtual_memory()
        return response.json({'memory_usage': memory_usage._asdict()})
    except Exception as e:
        return response.json({'error': str(e)}, status=500)

# 获取磁盘使用情况
@app.route('/disk_usage', methods=['GET'])
def get_disk_usage(request):
    try:
        disk_usage = psutil.disk_usage('/')
        return response.json({'disk_usage': disk_usage._asdict()})
    except Exception as e:
        return response.json({'error': str(e)}, status=500)

# 获取网络使用情况
@app.route('/network_usage', methods=['GET'])
def get_network_usage(request):
    try:
        network_usage = psutil.net_io_counters()
        return response.json({'network_usage': network_usage._asdict()})
# 添加错误处理
    except Exception as e:
        return response.json({'error': str(e)}, status=500)

# 运行Sanic应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
