# 代码生成时间: 2025-08-02 18:02:51
import json
from sanic import Sanic, response
from sanic.exceptions import ServerError, ClientError
from sanic.log import logger
def format_response(data, message, status_code):
    """
    Helper function to format API responses.
    :param data: The data to be sent in the response.
    :param message: A human-readable message.
    :param status_code: The HTTP status code.
    :return: Formatted JSON response.
    """
    response_data = {
        "data": data,
        "message": message
    }
    return response.json(response_data, status=status_code)

app = Sanic("APIResponseFormatter")

@app.exception(ServerError)
async def handle_server_error(request, exception):
    logger.error(f"Server error: {exception}")
    return format_response(
        None,
        "Internal Server Error",
        status_code=500
    )

@app.exception(ClientError)
async def handle_client_error(request, exception):
    logger.error(f"Client error: {exception}")
    return format_response(
        None,
        "Bad Request",
        status_code=400
    )

@app.route("/api/hello", methods=["GET"])
async def hello_world(request):
    try:
        # Simulate some processing
        name = request.args.get("name")
        if not name:
            raise ValueError("Name parameter is missing")
        return format_response(
            {
                "name": name
            },
            "Hello from the API",
            status_code=200
        )
    except ValueError as e:
        return format_response(
            None,
            str(e),
            status_code=400
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)