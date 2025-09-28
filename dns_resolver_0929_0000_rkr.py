# 代码生成时间: 2025-09-29 00:00:30
import asyncio
import aiodns
from sanic import Sanic, response
from sanic.exceptions import ServerError
from functools import lru_cache

# 定义DNS解析器和缓存工具
class DNSResolver:
    def __init__(self, resolver=None):
        self.resolver = resolver or aiodns.DNSResolver()
        self.cache = {}

    # DNS解析
    async def resolve(self, host):
        if host in self.cache:
            return self.cache[host]
        try:
            answer = await self.resolver.resolve(host)
            self.cache[host] = answer
            return answer
        except aiodns.error.DNSError as e:
            raise ServerError("DNS resolution failed: " + str(e))

    # 缓存装饰器
    def cache_decorator(func):
        def wrapper(self, *args, **kwargs):
            host = args[0]
            if host in self.cache:
                return self.cache[host]
            return func(self, *args, **kwargs)
        return wrapper

# 创建Sanic应用
app = Sanic("DNS Resolver")
resolver = DNSResolver()

# 定义路由
@app.route("/resolve", methods=["GET"])
@lru_cache(maxsize=100)  # 使用LRU缓存
async def resolve(request):
    host = request.args.get("host")
    if not host:
        return response.json("Host parameter is required", status=400)
    try:
        answer = await resolver.resolve(host)
        return response.json(answer)
    except ServerError as e:
        return response.json(str(e), status=500)

# 运行Sanic应用
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)