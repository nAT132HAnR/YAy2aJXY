# 代码生成时间: 2025-09-04 15:27:20
import asyncio
import aiohttp
from sanic import Sanic, response
from sanic.exceptions import ServerError, NotFound
from urllib.parse import urlparse

# 定义一个异步函数用于网页内容抓取
async def fetch_page_content(url):
    """
    Async function to fetch the page content from a given URL.

    :param url: The URL to fetch the content from.
    :return: The content of the page as a string if successful, otherwise None.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# 创建Sanic应用
app = Sanic("WebScraperApp")

# 定义一个路由处理函数，用于接收请求和返回网页内容
@app.route("/fetch", methods=["GET"])
async def fetch_handler(request):
    """
    Handle the GET request to fetch web page content.

    :param request: The Sanic request object.
    :return: A JSON response with the fetched webpage content.
    """
    url = request.args.get("url")
    if not url:
        raise NotFound("URL parameter is missing.")

    try:
        # 解析URL以确保其有效性
        parsed_url = urlparse(url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise ValueError("Invalid URL provided.")
        # 调用网页内容抓取函数
        page_content = await fetch_page_content(url)
        if page_content:
            return response.json({"content": page_content})
        else:
            raise ServerError("Failed to fetch web page content.")
    except Exception as e:
        return response.json({"error": str(e)}, status=400)

# 运行Sanic应用
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
