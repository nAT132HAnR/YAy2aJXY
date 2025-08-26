# 代码生成时间: 2025-08-27 05:20:06
import os
import base64
from cryptography.fernet import Fernet
from sanic import Sanic, response
from sanic.exceptions import ServerError

# 初始化Sanic应用
app = Sanic('PasswordCryptoService')

# 生成密钥
def generate_key():
    return Fernet.generate_key()

# 加密函数
def encrypt_message(message, key):
    try:
        fernet = Fernet(key)
        encrypted_message = fernet.encrypt(message.encode())
        return encrypted_message.decode()
    except Exception as e:
        raise ServerError(str(e))

# 解密函数
def decrypt_message(encrypted_message, key):
    try:
        fernet = Fernet(key)
        decrypted_message = fernet.decrypt(encrypted_message.encode())
        return decrypted_message.decode()
    except Exception as e:
        raise ServerError(str(e))

# 定义加密路由
@app.route("/encrypt", methods=["POST"])
async def encrypt(request):
    """
    加密密码
    :param request: 包含密码的请求
    :return: 加密后的密码
    """
    key = request.json.get("key")
    message = request.json.get("message")
    if not key or not message:
        return response.json({"error": "Missing key or message"}, status=400)
    return response.json({"encrypted": encrypt_message(message, key)})

# 定义解密路由
@app.route("/decrypt", methods=["POST"])
async def decrypt(request):
    """
    解密密码
    :param request: 包含加密密码和密钥的请求
    :return: 解密后的密码
    """
    key = request.json.get("key")
    encrypted_message = request.json.get("encrypted")
    if not key or not encrypted_message:
        return response.json({"error": "Missing key or encrypted message"}, status=400)
    return response.json({"decrypted": decrypt_message(encrypted_message, key)})

# 程序入口点
if __name__ == '__main__':
    # 生成密钥
    key = generate_key()
    # 保存密钥到环境变量
    os.environ['FERNET_KEY'] = key.decode()
    # 运行应用
    app.run(port=8000, host='0.0.0.0')