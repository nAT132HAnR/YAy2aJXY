# 代码生成时间: 2025-09-22 10:03:32
import unittest
from sanic import Sanic, response
from sanic.testing import SanicTestClient
from sanic.exceptions import ServerError


# Define a Sanic app for testing
app = Sanic('TestApp')

# Define a route for the app
@app.route('/test', methods=['GET'])
async def test(request):
    """
    Test route handler.
    Returns a simple message.
    """
    return response.json({'message': 'Hello, World!'})


# Define a test suite for the app
class TestSanicApp(unittest.TestCase):
    """
    Test suite for the Sanic application.
    """
    def setUp(self):
        """
        Set up a test client for the Sanic application.
        """
        self.app = app
        self.client = SanicTestClient(self.app)

    def test_get(self):
        """
        Test the GET request to the /test route.
        """
        response = self.client.get('/test')
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, {'message': 'Hello, World!'})

    def test_error(self):
        """
        Test for any unexpected errors.
        """
        with self.assertRaises(ServerError):
            self.client.get('/nonexistent')


# Run the tests if the script is executed directly
if __name__ == '__main__':
    unittest.main()