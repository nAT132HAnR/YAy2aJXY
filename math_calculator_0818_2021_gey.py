# 代码生成时间: 2025-08-18 20:21:26
import sanic
from sanic.response import json

# 使用Sanic创建一个数学计算工具集的Web服务
app = sanic.Sanic("MathCalculator")

# 定义一个数学计算类
class MathCalculator:
    def add(self, a, b):
        """两个数相加"""
        return a + b

    def subtract(self, a, b):
        """两个数相减"""
        return a - b

    def multiply(self, a, b):
        """两个数相乘"""
        return a * b

    def divide(self, a, b):
        """两个数相除"""
        try:
            return a / b
        except ZeroDivisionError:
            return "Cannot divide by zero"

# 实例化数学计算类
calculator = MathCalculator()

# 添加路由处理数学计算请求
@app.route("/add", methods=["GET"])
async def add(request):
    a = request.args.get("a")
    b = request.args.get("b")
    try:
        result = calculator.add(float(a), float(b))
        return json({"result": result})
    except ValueError:
        return json({"error": "Invalid input"}, status=400)

@app.route("/subtract", methods=["GET"])
async def subtract(request):
    a = request.args.get("a")
    b = request.args.get("b")
    try:
        result = calculator.subtract(float(a), float(b))
        return json({"result": result})
    except ValueError:
        return json({"error": "Invalid input"}, status=400)

@app.route("/multiply", methods=["GET"])
async def multiply(request):
    a = request.args.get("a")
    b = request.args.get("b")
    try:
        result = calculator.multiply(float(a), float(b))
        return json({"result": result})
    except ValueError:
        return json({"error": "Invalid input"}, status=400)

@app.route("/divide", methods=["GET"])
async def divide(request):
    a = request.args.get("a")
    b = request.args.get("b")
    try:
        result = calculator.divide(float(a), float(b))
        return json({"result": result})
    except ValueError:
        return json({"error": "Invalid input"}, status=400)
    except ZeroDivisionError:
        return json({"error": "Cannot divide by zero"}, status=400)

# 运行Sanic应用
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)