# 代码生成时间: 2025-08-01 00:47:06
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import json
from typing import Dict, List, Optional
from uuid import uuid4

# ShoppingCart is a class to manage shopping cart items
class ShoppingCart:
    def __init__(self):
        self.carts = {}

    def add_item(self, session_id: str, item_id: str, quantity: int) -> bool:
        """Add an item to the cart with the given quantity."""
        if session_id not in self.carts:
            self.carts[session_id] = {}
        self.carts[session_id][item_id] = quantity
        return True

    def remove_item(self, session_id: str, item_id: str) -> bool:
        """Remove an item from the cart."""
        if session_id in self.carts and item_id in self.carts[session_id]:
            del self.carts[session_id][item_id]
            return True
        return False

    def get_cart(self, session_id: str) -> Optional[Dict[str, int]]:
        """Get the cart for the given session_id."""
        return self.carts.get(session_id, None)

    def clear_cart(self, session_id: str) -> bool:
        """Clear the cart for the given session_id."""
        if session_id in self.carts:
            del self.carts[session_id]
            return True
        return False

# Initialize the Sanic app
app = Sanic("ShoppingCartAPI")

# Initialize the ShoppingCart class
shopping_cart = ShoppingCart()

# Endpoint to add an item to the shopping cart
@app.route(
    "/add_to_cart", methods=["POST"]
)
async def add_to_cart(request: Request) -> response.HTTPResponse:
    session_id = request.json.get("session_id")
    item_id = request.json.get("item_id")
    quantity = request.json.get("quantity", 1)

    if not session_id or not item_id or quantity <= 0:
        return json({"error": "Invalid request"}, status=400)

    if shopping_cart.add_item(session_id, item_id, quantity):
        return json({"message": "Item added to cart"}, status=201)
    else:
        return json({"error": "Failed to add item to cart"}, status=500)

# Endpoint to remove an item from the shopping cart
@app.route(
    "/remove_from_cart", methods=["POST"]
)
async def remove_from_cart(request: Request) -> response.HTTPResponse:
    session_id = request.json.get("session_id")
    item_id = request.json.get("item_id")

    if not session_id or not item_id:
        return json({"error": "Invalid request"}, status=400)

    if shopping_cart.remove_item(session_id, item_id):
        return json({"message": "Item removed from cart"}, status=200)
    else:
        return json({"error": "Failed to remove item from cart"}, status=500)

# Endpoint to get the shopping cart
@app.route(
    "/get_cart", methods=["GET"]
)
async def get_cart(request: Request) -> response.HTTPResponse:
    session_id = request.args.get("session_id")

    if not session_id:
        return json({"error": "Session ID is required"}, status=400)

    cart = shopping_cart.get_cart(session_id)
    if cart:
        return json(cart, status=200)
    else:
        return json({"error": "Cart not found"}, status=404)

# Endpoint to clear the shopping cart
@app.route(
    "/clear_cart", methods=["POST"]
)
async def clear_cart(request: Request) -> response.HTTPResponse:
    session_id = request.json.get("session_id")

    if not session_id:
        return json({"error": "Session ID is required"}, status=400)

    if shopping_cart.clear_cart(session_id):
        return json({"message": "Cart cleared"}, status=200)
    else:
        return json({"error": "Failed to clear cart"}, status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)