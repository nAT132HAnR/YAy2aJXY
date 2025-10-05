# 代码生成时间: 2025-10-06 03:04:21
from sanic import Sanic
from sanic.response import json

# 价格计算引擎
class PriceCalculator:
    def __init__(self):
        # 初始化价格计算引擎
        pass

    def calculate_price(self, base_price, discount):
        """
        计算价格

        :param base_price: 基础价格
        :param discount: 折扣
        :return: 最终价格
        """
        if discount < 0 or discount > 100:
            raise ValueError("折扣必须在0到100之间")

        return base_price * (1 - discount / 100)

# 定义Sanic应用
app = Sanic(__name__)

# 价格计算引擎实例
price_calculator = PriceCalculator()

@app.route("/price", methods=["GET"])
async def calculate_price(request):
    """
    计算价格的接口

    :param request: 请求对象
    :return: 计算结果
    """
    try:
        base_price = float(request.args.get("base_price", 0))
        discount = float(request.args.get("discount", 0))
        final_price = price_calculator.calculate_price(base_price, discount)
        return json({"base_price": base_price, "discount": discount, "final_price": final_price})
    except ValueError as e:
        return json({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)