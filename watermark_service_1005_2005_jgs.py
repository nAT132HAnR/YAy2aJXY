# 代码生成时间: 2025-10-05 20:05:42
import io
from sanic import Sanic, response
from sanic.request import Request
from PIL import Image, ImageDraw, ImageFont

# 数字水印服务的Sanic应用
app = Sanic("WatermarkService")

# 用于存放水印文本
WATERMARK_TEXT = "Your Watermark"
# 用于存放水印字体的路径
FONT_PATH = "/path/to/your/font.ttf"
# 水印的字体大小
FONT_SIZE = 20
# 水印的颜色
WATERMARK_COLOR = (255, 255, 255)  # White

# 处理POST请求，用于添加水印
@app.post("/add_watermark")
async def add_watermark(request: Request):
    # 获取上传的图片文件
    image_file = request.files.get("image")
    if not image_file:
        return response.json({
            "error": "No image file provided"
        }, status=400)

    try:
        # 打开图片文件
        image_stream = io.BytesIO(image_file.body)
        image = Image.open(image_stream)
        # 为图片创建一个绘图对象
        draw = ImageDraw.Draw(image)
        # 加载字体
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
        # 获取文本尺寸
        text_width, text_height = draw.textsize(WATERMARK_TEXT, font)
        # 设置水印位置
        watermark_pos = (image.width - text_width - 10, image.height - text_height - 10)
        # 在图片上添加水印
        draw.text(watermark_pos, WATERMARK_TEXT, font=font, fill=WATERMARK_COLOR)
        # 将修改后的图片保存到字节流中
        output_stream = io.BytesIO()
        image.save(output_stream, format=image.format)
        output_stream.seek(0)
        # 返回带有水印的图片
        return response.file(output_stream, filename="watermarked_image.jpg")
    except Exception as e:
        # 返回错误信息
        return response.json({
            "error": str(e)
        }, status=500)

# 运行Sanic应用
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)