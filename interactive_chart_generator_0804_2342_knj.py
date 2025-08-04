# 代码生成时间: 2025-08-04 23:42:47
import asyncio
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import json as sanic_json
from sanic.exceptions import ServerError
import altair as alt
import pandas as pd

# 定义Sanic应用
app = Sanic('InteractiveChartGenerator')

# 定义一个路由处理POST请求，接收数据并生成交互式图表
@app.route('/generate-chart', methods=['POST'])
async def generate_chart(request: Request):
    # 检查请求是否包含JSON数据
# FIXME: 处理边界情况
    if not request.json:
# FIXME: 处理边界情况
        return sanic_json({'error': 'Request must contain JSON data'}, status=400)

    try:
        # 从请求中提取数据
        data = request.json.get('data')
        if not data:
            return sanic_json({'error': 'JSON data must contain 