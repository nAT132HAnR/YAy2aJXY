# 代码生成时间: 2025-10-11 01:55:19
import asyncio
from sanic import Sanic, response
from sanic.views import CompositionView
from jinja2 import Environment, FileSystemLoader

# Define the path to the templates
TEMPLATE_PATH = "templates"

# Create the Sanic app
app = Sanic("ResponsiveApp")

# Configure the template environment
env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))

# Define the routes
@app.route("/")
async def home(request):
    # Load the template and render it
    template = env.get_template("index.html")
    return response.html(template.render(), content_type='text/html')

@app.route("/responsive")
async def responsive(request):
    try:
        # Load the template and render it
        template = env.get_template("responsive.html")
        return response.html(template.render(), content_type='text/html')
    except Exception as e:
        # Handle any exceptions that occur during template rendering
        return response.json({
            "error": str(e)
        }, status=500)

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
