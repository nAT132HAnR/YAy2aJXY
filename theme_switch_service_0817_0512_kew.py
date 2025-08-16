# 代码生成时间: 2025-08-17 05:12:41
import asyncio
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import json
from sanic.exceptions import ServerError, ServerNotReady, ClientError, NotFound


# Define a custom exception for unsupported themes
class UnsupportedThemeError(Exception):
    pass


# Define the available themes
AVAILABLE_THEMES = {'light', 'dark', 'colorful'}


# Initialize the Sanic application
app = Sanic("ThemeSwitchService")


@app.listener("before_server_start")
async def setup_themes(request: Request):
    # Initialize a set to store current active themes
    app.ctx.themes = set()


@app.listener("after_server_stop\)
async def teardown_themes(request: Request):
    # Clean up the themes on server stop
    app.ctx.themes = None


@app.route("/switch_theme", methods=["POST"])
async def switch_theme(request: Request):
    # Extract the theme from the request body
    theme = request.json.get("theme", None)

    # Check if the theme is supported
    if theme not in AVAILABLE_THEMES:
        # Return an error response if the theme is unsupported
        return json({
            "error": "unsupported_theme",
            "message": f"The theme '{theme}' is not supported."
        }, status=400)

    # Toggle the theme in the set of active themes
    if theme in app.ctx.themes:
        app.ctx.themes.remove(theme)
    else:
        app.ctx.themes.add(theme)

    # Return the updated list of active themes
    return json({
        "active_themes": list(app.ctx.themes)
    })


if __name__ == '__main__':
    # Run the Sanic application
    app.run(host="0.0.0.0", port=8000, debug=True)