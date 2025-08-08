# 代码生成时间: 2025-08-08 13:16:12
import sanic
from sanic.response import json, html
from sanic.exceptions import ServerError
import plotly
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# Define the Sanic app
app = sanic.Sanic("InteractiveChartGenerator")

# Home page route
@app.route("/", methods=["GET"])
async def home(request):
    # Return the HTML page for the user to interact with
    return html("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Interactive Chart Generator</title>
    </head>
    <body>
        <h1>Interactive Chart Generator</h1>
        <form action="/generate-chart" method="post">
            <label for="data">Enter data as CSV:</label><br>
            <textarea id="data" name="data" rows="4" cols="50"></textarea><br>
            <input type="submit" value="Generate Chart">
        </form>
    </body>
    </html>
    """)

# Route to generate the chart
@app.route("/generate-chart", methods=["POST"])
async def generate_chart(request):
    try:
        # Get the data from the form
        data = request.form.get("data")
        if not data:
            raise ValueError("No data provided")

        # Create a DataFrame from the provided CSV data
        df = pd.read_csv(pd.compat.StringIO(data))
        
        # Create a subplot with two subplots
        fig = make_subplots(rows=2, cols=1, subplot_titles=('Line Plot', 'Scatter Plot'))
        
        # Generate a line plot
        fig.add_trace(plotly.graph_objects.Scatter(x=df.columns[0], y=df.columns[1]), row=1, col=1)
        
        # Generate a scatter plot
        fig.add_trace(plotly.graph_objects.Scatter(x=df.columns[0], y=df.columns[1]), row=2, col=1)
        
        # Update layout
        fig.update_layout(height=600, width=800, title_text="Interactive Chart")
        
        # Return the chart as HTML
        return html(fig.to_html())
    except Exception as e:
        # Handle any errors and return a JSON response
        raise ServerError("An error occurred: " + str(e))
        
# Run the Sanic app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
