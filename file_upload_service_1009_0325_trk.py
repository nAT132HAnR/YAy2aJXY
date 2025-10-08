# 代码生成时间: 2025-10-09 03:25:21
import os
from sanic import Sanic, response
from sanic.request import Request
from sanic.handlers import ErrorHandler
from sanic.exceptions import ServerError
from sanic.log import logger

# 文件上传服务配置
UPLOAD_FOLDER = "./uploads/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 检查文件扩展名是否被允许
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 初始化Sanic应用
app = Sanic("FileUploadService")

# 上传文件的路由
@app.route("/upload", methods=["POST"])
async def file_upload(request: Request):
    # 获取上传的文件
    file = request.files.get("file")
    if file is None:
        return response.json({
            "error": "No file part"
        }, status=400)

    if not allowed_file(file.name):
        return response.json({
            "error": f"File type {file.name.rsplit('.', 1)[1].lower()} is not allowed"
        }, status=400)

    # 保存文件到指定目录
    save_path = os.path.join(UPLOAD_FOLDER, file.name)
    with open(save_path, "wb") as f:
        f.write(await file.read())

    return response.json({
        "message": "File uploaded successfully", 
        "filepath": save_path
    })

# 错误处理器
class MyErrorHandler(ErrorHandler):
    async def default(self, request, exception):
        logger.error(f"Unhandled exception: {exception}")
        return response.json({"error": str(exception)}, status=500)

# 设置错误处理器
app.error_handler.add_exception(ServerError, MyErrorHandler())

# 运行Sanic应用
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)