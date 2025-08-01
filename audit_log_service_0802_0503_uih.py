# 代码生成时间: 2025-08-02 05:03:54
from sanic import Sanic, response
from sanic.log import logger
import json
import logging
from datetime import datetime

# Define the configuration for the logging
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True
        },
    }
}

# Initialize the Sanic application
app = Sanic("AuditLogService")

# Middleware to capture request and response data for logging
@app.middleware('request')
async def log_request(request):
    """
    Middleware to log the incoming request.
    """
    await asyncio.sleep(0)  # Ensure this runs before request handler
    request.ctx.start_time = datetime.now()

@app.middleware('response')
async def log_response(request, response):
    """
    Middleware to log the response and the duration of the request.
    """
    await asyncio.sleep(0)  # Ensure this runs after response handler
    request_time = (datetime.now() - request.ctx.start_time).total_seconds()
    logger.info(f"{request.method} {request.url.path} - Status: {response.status} - Time: {request_time}s")

# Route to handle the audit log requests
@app.route('/api/audit', methods=['POST'])
async def audit_log(request):
    """
    Endpoint to receive audit log data and log it.
    """
    try:
        data = request.json
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event': data.get('event'),
            'details': data.get('details')
        }
        logger.info(json.dumps(log_entry))
        return response.json({'status': 'success', 'message': 'Log entry created successfully'})
    except Exception as e:
        logger.error(f"Error processing audit log request: {e}")
        return response.json({'status': 'error', 'message': 'Failed to create log entry'}, status=500)

# Run the application
if __name__ == '__main__':
    logging.config.dictConfig(LOGGING_CONFIG)
    app.run(host='0.0.0.0', port=8000)