# 代码生成时间: 2025-10-10 01:34:49
from sanic import Sanic
from sanic.response import json
from sanic.exceptions import ServerError, ClientError, VersionNotSupported
import math

# 创建一个Sanic应用
app = Sanic("MathCalculatorService")

# 定义一个数学计算工具集
class MathCalculator:
    def add(self, a, b):
        """Add two numbers.
        Args:
            a (float): The first number.
            b (float): The second number.
        Returns:
            float: The sum of the two numbers.
        """
        return a + b

    def subtract(self, a, b):
        """Subtract one number from another.
        Args:
            a (float): The first number.
            b (float): The second number.
        Returns:
            float: The difference of the two numbers.
        """
        return a - b

    def multiply(self, a, b):
        """Multiply two numbers.
        Args:
            a (float): The first number.
            b (float): The second number.
        Returns:
            float: The product of the two numbers.
        """
        return a * b

    def divide(self, a, b):
        """Divide one number by another.
        Args:
            a (float): The first number.
            b (float): The second number.
        Returns:
            float: The quotient of the two numbers.
        Raises:
            ZeroDivisionError: If the second number is zero.
        """
        try:
            return a / b
        except ZeroDivisionError:
            raise ClientError("Cannot divide by zero", status_code=400)

    def power(self, a, b):
        """Raise a number to a power.
        Args:
            a (float): The base number.
            b (float): The exponent.
        Returns:
            float: The result of the exponentiation.
        """
        return math.pow(a, b)

# 实例化数学计算工具集
calculator = MathCalculator()

# 添加路由以处理加法请求
@app.route("/add", methods=["POST"])
async def add(request):
    data = request.json
    try:
        result = calculator.add(data["a"], data["b"])
        return json({