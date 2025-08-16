# 代码生成时间: 2025-08-16 14:26:37
import json
from sanic import Sanic, response
from sanic.exceptions import ServerError, abort
from sanic.response import json as json_response

# 库存管理应用
app = Sanic("InventoryManagementSystem")

# 模拟数据库
inventory = {"items": []}

# 添加库存项
@app.route("/inventory", methods=["POST"])
async def add_inventory(request):
    # 解析请求体中的JSON数据
    data = request.json
    # 验证数据
    if not data or 'name' not in data or 'quantity' not in data:
        return json_response({"error": "Missing item name or quantity"}, status=400)
    # 添加到库存
    inventory["items"].append(data)
    return json_response({"message": "Item added successfully"}, status=201)

# 获取所有库存项
@app.route("/inventory", methods=["GET"])
async def get_inventory(request):
    return json_response(inventory)

# 更新库存项
@app.route("/inventory/<item_id:int>", methods=["PUT"])
async def update_inventory(request, item_id):
    data = request.json
    # 查找库存项
    item = next((item for item in inventory["items"] if item.get("id") == item_id), None)
    if not item:
        abort(404, "Item not found")
    # 更新库存项
    if 'name' in data and 'quantity' in data:
        item['name'] = data['name']
        item['quantity'] = data['quantity']
    return json_response({"message": "Item updated successfully"}, status=200)

# 删除库存项
@app.route("/inventory/<item_id:int>", methods=["DELETE"])
async def delete_inventory(request, item_id):
    # 查找库存项
    item = next((item for item in inventory["items"] if item.get("id") == item_id), None)
    if not item:
        abort(404, "Item not found")
    # 删除库存项
    inventory["items"] = [item for item in inventory["items"] if item.get("id") != item_id]
    return json_response({"message": "Item deleted successfully"}, status=200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)