# 代码生成时间: 2025-09-08 16:25:14
import asyncio
import json
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import HTTPResponse
from sanic.exceptions import ServerError
from sanic_cors import CORS  # 使用sanic_cors实现跨域请求支持


# 数据统计和分析类
class DataAnalyzer:
    def __init__(self, data):
        self.data = data

    def calculate_mean(self):
        """计算数据的平均值。"""
        return sum(self.data) / len(self.data) if self.data else 0

    def calculate_median(self):
        """计算数据的中位数。"""
        sorted_data = sorted(self.data)
        n = len(sorted_data)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_data[mid - 1] + sorted_data[mid]) / 2
        else:
            return sorted_data[mid]

    def calculate_mode(self):
        """计算数据的众数。"""
        from collections import Counter
        return Counter(self.data).most_common(1)[0][0] if self.data else None


# 应用配置
app = Sanic(__name__)
CORS(app)  # 允许跨域请求


# 数据分析器路由处理器
@app.route("/analyze", methods=["POST"])
async def analyze_data(request: Request):
    try:
        data = request.json
        if not isinstance(data, list) or not all(isinstance(x, (int, float)) for x in data):
            return response.json({
                "error": "Invalid data format. Please provide a list of numbers."
            }, status=400)

        analyzer = DataAnalyzer(data)
        results = {
            "mean": analyzer.calculate_mean(),
            "median": analyzer.calculate_median(),
            "mode": analyzer.calculate_mode()
        }
        return response.json(results)
    except Exception as e:
        return response.json({
            "error": str(e)
        }, status=500)

# 启动应用
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)