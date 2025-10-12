# 代码生成时间: 2025-10-12 21:29:59
import asyncio
from sanic import Sanic, response
from sanic.response import json
from sanic.exceptions import ServerError

# 初始化Sanic应用
app = Sanic("Member Management System")

# 会员数据存储结构
members = []

# 会员数据模型
class Member:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }

# 会员列表接口
@app.route("/members", methods=["GET"])
async def get_members(request):
    """
    获取所有会员信息
    """
    return response.json([m.to_dict() for m in members])

# 添加会员接口
@app.route("/members", methods=["POST"])
async def add_member(request):
    data = request.json
    if not data or "name" not in data or "email" not in data:
        return response.json({
            "error": "There was a problem with your request."
        }, status=400)
    member = Member(len(members) + 1, data["name"], data["email"])
    members.append(member)
    return response.json(member.to_dict(), status=201)

# 获取单个会员信息接口
@app.route("/members/<int:member_id>", methods=["GET"])
async def get_member(request, member_id):
    """
    通过会员ID获取单个会员信息
    """
    member = next((m for m in members if m.id == member_id), None)
    if member is None:
        return response.json({
            "error": "Member not found."
        }, status=404)
    return response.json(member.to_dict())

# 更新会员信息接口
@app.route("/members/<int:member_id>", methods=["PUT"])
async def update_member(request, member_id):
    data = request.json
    member = next((m for m in members if m.id == member_id), None)
    if member is None:
        return response.json({
            "error": "Member not found."
        }, status=404)
    if "name" in data:
        member.name = data["name"]
    if "email" in data:
        member.email = data["email"]
    return response.json(member.to_dict())

# 删除会员信息接口
@app.route("/members/<int:member_id>", methods=["DELETE"])
async def delete_member(request, member_id):
    """
    通过会员ID删除会员信息
    """
    global members
    members = [m for m in members if m.id != member_id]
    return response.json({
        "message": "Member deleted successfully."
    }, status=200)

# 运行Sanic应用
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)