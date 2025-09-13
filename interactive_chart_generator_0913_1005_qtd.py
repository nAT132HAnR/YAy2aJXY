# 代码生成时间: 2025-09-13 10:05:17
import asyncio
from sanic import Sanic, response
from sanic.request import Request
from sanic.exceptions import ServerError
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# 创建Sanic应用
app = Sanic("Interactive Chart Generator")

# 定义图表数据
def get_sample_data():
    """
    返回示例数据点以用于图表。
    """
    # 这里可以使用实际的数据源
    x = [1, 2, 3, 4, 5]
    y = [2, 3, 5, 7, 11]
    return x, y

# 定义生成图表的函数
def generate_chart(x, y):
    """
    根据数据点生成图表
    """
    plt.figure()
    plt.plot(x, y)
    plt.xlabel('X Axis Label')
    plt.ylabel('Y Axis Label')
    plt.title('Interactive Chart')
    
    # 将图表保存到字节流中
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    # 编码图片为base64字符串
    img_str = base64.b64encode(buffer.read()).decode()
    plt.close()
    return img_str

# 定义Sanic路由处理函数
@app.route("/chart", methods=["GET"])
async def chart(request: Request):
    """
    处理生成图表的请求。
    """
    try:
        # 获取示例数据
        x, y = get_sample_data()
        # 生成图表
        img_str = generate_chart(x, y)
        # 响应图片数据
        return response.json({
            "status": "success",
            "image": f"data:image/png;base64,{img_str}"
        })
    except Exception as e:
        # 错误处理
        return response.json({
            "status": "error",
            "message": str(e)
        }, status=500)

# 定义启动应用的函数
def run_app():
    """
    运行Sanic应用。
    """
    app.run(host="0.0.0.0", port=8000, debug=True)

# 程序入口点
if __name__ == '__main__':
    run_app()