# 代码生成时间: 2025-09-23 18:22:35
import os
import asyncio
from sanic import Sanic, response
from jinja2 import Environment, FileSystemLoader

# 定义全局变量，用于存放模板文件夹路径
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')

# 创建 Sanic 应用
app = Sanic('ResponsiveLayoutSanic')

# 设置 Jinja2 模板加载器
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

# 定义路由，用于返回首页视图
@app.route('/')
async def home(request):
    # 渲染模板并返回响应
    template = env.get_template('home.html')
    return response.html(template.render())

# 定义路由，用于返回响应式布局测试视图
@app.route('/responsive')
async def responsive(request):
    # 渲染模板并返回响应
    template = env.get_template('responsive.html')
    return response.html(template.render())

# 定义错误处理函数
@app.exception(404)
async def not_found404(request, exception):
    # 返回 404 错误页面
    return response.html("<h1>404 Not Found</h1>", status=404)

# 定义异常处理函数
@app.exception(Exception)
async def handle_exception(request, exception):
    # 日志记录异常信息
    print(f"Exception: {exception}")
    # 返回 500 错误页面
    return response.html("<h1>500 Internal Server Error</h1>", status=500)

# 运行 Sanic 应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
