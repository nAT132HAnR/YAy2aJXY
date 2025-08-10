# 代码生成时间: 2025-08-11 06:05:41
import sanic
from sanic.response import json
from urllib.parse import urlparse
import requests
from sanic.exceptions import ServerError

# 定义一个类，用于URL链接有效性验证
class URLValidatorService:
    def __init__(self):
        # 初始化Sanic应用
        self.app = sanic.Sanic("URLValidatorService")

        # 定义路由 /validate-url
        @self.app.route('/validate-url', methods=['POST'])
        async def validate_url(request):
            # 从请求中获取URL数据
            url_data = request.json.get('url')

            # 检查URL是否为空
            if not url_data:
                return json({'error': 'URL is required'}, status=400)

            try:
                # 解析URL
                parsed_url = urlparse(url_data)

                # 检查协议是否有效
                if not parsed_url.scheme or not parsed_url.netloc:
                    return json({'error': 'Invalid URL format'}, status=400)

                # 使用requests库验证URL是否可以访问
                response = requests.head(url_data, allow_redirects=True, timeout=5)
                if response.status_code != 200:
                    return json({'error': 'URL is not accessible'}, status=400)

                # 返回成功验证的结果
                return json({'message': 'URL is valid'}, status=200)

            except requests.RequestException as e:
                # 捕获请求异常
                return json({'error': 'Failed to validate URL'}, status=500)
            except Exception as e:
                # 捕获其他异常
                raise ServerError(f"An error occurred: {str(e)}")

    def run(self):
        # 运行Sanic应用
        self.app.run(host='0.0.0.0', port=8000, workers=1)

# 创建URLValidatorService实例
url_validator_service = URLValidatorService()

# 运行服务
if __name__ == '__main__':
    url_validator_service.run()