# 代码生成时间: 2025-08-10 06:45:05
import sanic
from sanic.response import json, text
from sanic.exceptions import ServerError, abort
from sanic.security import HTTPBasicAuth, HTTPDigestAuth
from sanic.config import Config

# Configuration
config = Config(ACCESS_LOG=False)

app = sanic.Sanic('Access Control Example', config=config)

# Dummy user database
users = {
    'admin': 'password123',
    'user': 'password456'
}

# Middleware for authentication
def authenticate(request):
    auth = request.headers.get('Authorization')
    if not auth:
        return False
    auth_type, token = auth.split()
    if auth_type == 'Basic':
        username, password = token.decode('base64').split(':')
        if username in users and users[username] == password:
            return True
    return False

# Middleware for access control
def access_control(request):
    if not authenticate(request):
        raise ServerError(text="Unauthorized", status_code=401)

# Define routes
@app.route('/admin', methods=['GET'], middleware=[access_control])
async def admin_access(request):
    return json({'message': 'Access to admin panel granted'})

@app.route('/user', methods=['GET'])
async def user_access(request):
    return json({'message': 'Access to user panel granted'})

@app.exception(ServerError)
async def handle_server_error(request, exception):
    return json({'error': str(exception)}, status=exception.status_code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, auto_reload=False)