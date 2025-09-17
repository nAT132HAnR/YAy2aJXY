# 代码生成时间: 2025-09-18 03:05:50
import sanic
from sanic.response import json
from sanic.exceptions import ServerError
from sanic import Blueprint
from sanic.views import CompositionView

# User permission management blueprint
permission_bp = Blueprint('permission', url_prefix='/permission')

# User model (simplified for demonstration purposes)
class User:
    def __init__(self, username, permissions):
        self.username = username
        self.permissions = permissions

# In-memory user store (for demonstration purposes)
users = {
    'admin': User('admin', ['read', 'write', 'delete']),
    'user': User('user', ['read']),
}

# Check if user has the required permission
def has_permission(user, permission):
    """Check if the user has the specified permission."""
    return permission in user.permissions

# API endpoint to check user permissions
@permission_bp.route('/check', methods=['POST'])
async def check_permission(request):
    data = request.json
    username = data.get('username')
    permission = data.get('permission')
    user = users.get(username)
    
    if user is None:
        return json({'error': 'User not found'}, status=404)
    if not has_permission(user, permission):
        return json({'error': 'Permission denied'}, status=403)
    return json({'message': 'Permission granted'})

# Main app
app = sanic.Sanic('User Permission Management')
app.blueprint(permission_bp)

# Error handler for 404 errors
@app.exception(ServerError)
async def server_error_exception_handler(request, exception):
    return json({'error': 'Internal Server Error'}, status=500)

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)