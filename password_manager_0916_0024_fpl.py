# 代码生成时间: 2025-09-16 00:24:48
import base64
import hashlib
import hmac
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import HTTPResponse
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

# 初始化密钥
KEY = Fernet.generate_key()
fernet = Fernet(KEY)

app = Sanic("PasswordManager")

# 生成RSA密钥对
def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return pem, public_pem

# RSA加密
def rsa_encrypt(public_key, message):
    public_key = serialization.load_pem_public_key(
        public_key,
        backend=default_backend()
    )
    encrypted = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted

# RSA解密
def rsa_decrypt(private_key, message):
    private_key = serialization.load_pem_private_key(
        private_key,
        password=None,
        backend=default_backend()
    )
    decrypted = private_key.decrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted

# 加密密码
@app.route("/encrypt", methods=["POST"])
async def encrypt_password(request: Request):
    data = request.json
    password = data.get("password")
    if not password:
        return response.json({"error": "Missing password parameter"}, status=400)
    try:
        # 使用Fernet进行密码加密
        encrypted_password = fernet.encrypt(password.encode()).decode()
        return response.json({"encrypted_password": encrypted_password})
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

# 解密密码
@app.route("/decrypt", methods=["POST"])
async def decrypt_password(request: Request):
    data = request.json
    encrypted_password = data.get("encrypted_password")
    if not encrypted_password:
        return response.json({"error": "Missing encrypted_password parameter"}, status=400)
    try:
        # 使用Fernet进行密码解密
        decrypted_password = fernet.decrypt(encrypted_password.encode()).decode()
        return response.json({"decrypted_password": decrypted_password})
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

# 生成RSA密钥对
@app.route("/generate_keys", methods=["GET"])
async def generate_rsa_keys_endpoint(request: Request):
    try:
        private_key, public_key = generate_rsa_keys()
        return response.json({"private_key": private_key.decode(), "public_key": public_key.decode()})
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

# RSA加密密码
@app.route("/rsa_encrypt", methods=["POST"])
async def rsa_encrypt_password(request: Request):
    data = request.json
    password = data.get("password")
    public_key = data.get("public_key")
    if not password or not public_key:
        return response.json({"error": "Missing password or public_key parameter"}, status=400)
    try:
        encrypted_password = rsa_encrypt(public_key.encode(), password.encode())
        return response.json({"encrypted_password": base64.b64encode(encrypted_password).decode()})
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

# RSA解密密码
@app.route("/rsa_decrypt", methods=["POST"])
async def rsa_decrypt_password(request: Request):
    data = request.json
    encrypted_password = data.get("encrypted_password")
    private_key = data.get("private_key")
    if not encrypted_password or not private_key:
        return response.json({"error": "Missing encrypted_password or private_key parameter"}, status=400)
    try:
        decrypted_password = rsa_decrypt(private_key.encode(), base64.b64decode(encrypted_password))
        return response.json({"decrypted_password": decrypted_password.decode()})
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)