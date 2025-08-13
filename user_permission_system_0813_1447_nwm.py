# 代码生成时间: 2025-08-13 14:47:55
import asyncio
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import json
from sanic.exceptions import ServerError, NotFound

# User model to represent user data
class User:
    def __init__(self, username, permissions):
        self.username = username
        self.permissions = permissions

# UserPermissionService handles user permission logic
class UserPermissionService:
    def __init__(self):
        self.users = {}

    def add_user(self, username, permissions):
        if username in self.users:
            raise ValueError("User already exists")
        self.users[username] = User(username, permissions)

    def check_permission(self, username, permission):
        user = self.users.get(username)
        if not user:
            raise NotFound("User not found")
        if permission not in user.permissions:
            raise Forbidden("Permission denied")
        return True

# Custom exceptions for user permission system
class Forbidden(Exception):
    pass

# Sanic application
app = Sanic("UserPermissionSystem")
permission_service = UserPermissionService()

# Initialize user data
@app.listener("before_server_start")
async def setup_db(app, loop):
    permission_service.add_user("admin", ["read", "write", "delete"])
    permission_service.add_user("user", ["read"])

# Endpoint to check if a user has a specific permission
@app.route("/check_permission/<username>/<permission>", methods=["GET"])
async def check_permission(request: Request, username: str, permission: str):
    try:
        result = permission_service.check_permission(username, permission)
        return response.json({
            "message": "Permission check successful",
            "has_permission": result
        })
    except (ValueError, NotFound, Forbidden) as e:
        return response.json({
            "error": str(e),
            "code": 403 if isinstance(e, Forbidden) else 404
        }, status=e.__class__.__name__)

# Start the Sanic application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)