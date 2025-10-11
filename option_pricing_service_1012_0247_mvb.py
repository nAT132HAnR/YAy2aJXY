# 代码生成时间: 2025-10-12 02:47:33
import math
from sanic import Sanic, response
from sanic.log import logger

# 定义期权定价服务的异常类
class PricingError(Exception):
    pass

# 实现Black-Scholes模型进行欧式期权定价
def black_scholes(S, K, T, r, sigma):
    """
    Black-Scholes模型计算欧式期权价格
    :param S: 标的资产现价
    :param K: 执行价格
    :param T: 到期时间（以年为单位）
    :param r: 无风险利率
    :param sigma: 标的资产的年化波动率
    :return: 欧式看涨/看跌期权价格
    """
    d1 = (math.log(S / K) + (r + (sigma ** 2) / 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    call = (S * math.exp(-r * T) * norm.cdf(d1)) - (K * math.exp(-r * T) * norm.cdf(d2))
    put = call - S + K * math.exp(-r * T)
    return call, put

# 使用scipy库中的norm.cdf函数来计算标准正态分布的累积分布函数值
from scipy.stats import norm

app = Sanic("OptionPricingService")

@app.route("/price", methods=["GET"])
async def price_option(request):
    """
    HTTP接口，根据请求参数计算期权价格
    :param request: 包含请求参数的Sanic请求对象
    :return: 期权价格的JSON响应
    """
    try:
        S = float(request.args.get("S", 100))  # 标的资产现价，默认100
        K = float(request.args.get("K", 100))  # 执行价格，默认100
        T = float(request.args.get("T", 1))  # 到期时间，默认1年
        r = float(request.args.get("r", 0.05))  # 无风险利率，默认5%
        sigma = float(request.args.get("sigma\, 0.2))  # 波动率，默认20%

        call, put = black_scholes(S, K, T, r, sigma)

        return response.json({
            "call_price": call,
            "put_price": put
        })
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        return response.json({
            "error": "Invalid input parameters"
        }, status=400)
    except PricingError as e:
        logger.error(f"Pricing error: {e}")
        return response.json({
            "error": "Error calculating the option price"
        }, status=500)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return response.json({
            "error": "Unexpected error occurred"
        }, status=500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)