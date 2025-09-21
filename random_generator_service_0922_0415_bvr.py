# 代码生成时间: 2025-09-22 04:15:09
import sanic
from sanic.response import json
import random

"""
Random Number Generator Service
This service provides an API endpoint to generate random numbers.
"""

app = sanic.Sanic('random_generator_service')

@app.route('/random/<int:seed>/', methods=['GET'])
async def generate_random_number(request, seed):
    """
    Generates a random number based on the provided seed.

    :param request: The request object.
    :param seed: The random seed for generating the number.
    :return: A JSON response with the random number.
    """
    try:
        random.seed(seed)
        random_number = random.randint(0, 100)  # Generate a random number between 0 and 100
        return json({'random_number': random_number})
    except Exception as e:
        """
        Error handling for any exceptions that occur during the generation process.
        """
        return json({'error': str(e)}, status=500)

if __name__ == '__main__':
    """
    Runs the Sanic server if this script is executed as the main program.
    """
    app.run(host='0.0.0.0', port=8000)