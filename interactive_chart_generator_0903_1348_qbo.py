# 代码生成时间: 2025-09-03 13:48:34
import asyncio
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import json
import plotly.graph_objs as go
from plotly.offline import plot
import base64


# Initialize the Sanic app
app = Sanic("InteractiveChartGenerator")


# Function to create a simple line chart
def create_line_chart(x, y):
    # Create a trace
    trace = go.Scatter(x=x, y=y)
    # Create a layout
    layout = go.Layout(title="Line Chart", xaxis=dict(title="X Axis"), yaxis=dict(title="Y Axis"))
    # Create a figure
    fig = go.Figure(data=[trace], layout=layout)
    return fig


# Endpoint to generate chart
@app.route("/chart", methods=["GET"])
async def chart(request: Request):
    # Get query parameters
    x = request.args.get("x")
    y = request.args.get("y")
    
    # Error checking
    if not x or not y:
        return json({"error": "Missing query parameters"}, status=400)
    
    try:
        # Convert query parameters from string to list of floats
        x = [float(i) for i in x.split(",")]
        y = [float(i) for i in y.split(",")]
    except ValueError:
        return json({"error": "Invalid input format"}, status=400)
    
    # Create the chart
    fig = create_line_chart(x, y)
    
    # Plot the figure to a byte array and encode it to base64
    plot(fig, filename="tmp_plot.html", auto_open=False)
    with open("tmp_plot.html", "rb") as image_file:
        plot_html_b64 = base64.b64encode(image_file.read()).decode("utf-8")
    
    # Return the chart as a JSON response
    return json({"chart": plot_html_b64})


# Run the Sanic app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
