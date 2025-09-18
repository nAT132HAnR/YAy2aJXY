# 代码生成时间: 2025-09-18 17:18:43
from sanic import Sanic, response
from sanic.exceptions import ServerError, abort
from urllib.parse import urlparse
import validators


# 创建一个Sanic应用
app = Sanic("UrlValidatorService")

"""
API端点：检查URL是否有效
路径：/validate-url
方法：POST
输入：JSON格式的URL字符串
输出：JSON格式的有效性结果
"""
@app.post("/validate-url")
async def validate_url(request):
    # 从请求体中获取URL
    url = request.json.get("url")
    if not url:
        # 如果URL为空，返回400错误
        abort(400, "URL is missing")

    try:
        # 使用validators模块验证URL
        is_valid = validators.url(url)
        if is_valid:
            # 如果URL有效，返回200状态码和有效性信息
            return response.json({
                "status": "success",
                "message": "URL is valid",
                "data": {"url": url}
            })
        else:
            # 如果URL无效，返回200状态码和无效性信息
            return response.json({
                "status": "error",
                "message": "URL is invalid",
                "data": {"url": url}
            })
    except Exception as e:
        # 捕捉并返回任何异常
        raise ServerError("Error validating URL