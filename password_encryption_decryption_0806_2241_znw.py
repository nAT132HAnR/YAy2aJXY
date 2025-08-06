# 代码生成时间: 2025-08-06 22:41:09
import sanic
from sanic.response import json
from cryptography.fernet import Fernet

# 定义加密密钥
# 注意：在生产环境中，密钥应该安全地存储和访问
SECRET_KEY = 'your_secret_key_here'
fernet = Fernet(SECRET_KEY)

app = sanic.Sanic("PasswordEncryptionDecryption")

# 定义加密端点
@app.route("/encrypt", methods=["POST"])
async def encrypt(request):
    # 获取请求体中的数据
    data = request.json
    if not data or 'password' not in data:
        return json({'error': 'Missing password in request'}, status=400)
    
    # 加密密码
    try:
        encrypted_password = fernet.encrypt(data['password'].encode()).decode()
        return json({'encrypted_password': encrypted_password})
    except Exception as e:
        return json({'error': str(e)}, status=500)

# 定义解密端点
@app.route("/decrypt", methods=["POST"])
async def decrypt(request):
    # 获取请求体中的数据
    data = request.json
    if not data or 'encrypted_password' not in data:
        return json({'error': 'Missing encrypted password in request'}, status=400)
    
    # 解密密码
    try:
        decrypted_password = fernet.decrypt(data['encrypted_password'].encode()).decode()
        return json({'decrypted_password': decrypted_password})
    except Exception as e:
        return json({'error': str(e)}, status=500)

# 运行应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)