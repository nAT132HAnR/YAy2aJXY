# 代码生成时间: 2025-08-20 10:41:23
import asyncio
from sanic import Sanic, response
from sanic.exceptions import ServerError
from faker import Faker
from loguru import logger

# Initialize Faker for generating fake data
fake = Faker()

app = Sanic(__name__)

@app.route('/test-data', methods=['GET'])
async def generate_test_data(request):
    """
    Generate and return a JSON response containing fake data.
    The route handles GET requests to generate test data.
    """
    try:
        # Generate fake data
        fake_data = {
            "name": fake.name(),
            "email": fake.email(),
            "address": fake.address(),
            "phone_number": fake.phone_number(),
        }
        # Return the fake data as JSON
        return response.json(fake_data)
    except Exception as e:
        # Log and handle any exceptions that occur
        logger.error(f"An error occurred: {e}")
        raise ServerError("Failed to generate test data.")

if __name__ == '__main__':
    # Run the Sanic app
    logger.info("Starting Test Data Generator...")
    app.run(host='0.0.0.0', port=8000, workers=1)
