# 代码生成时间: 2025-08-25 20:52:59
import sanic
from sanic.response import json
from peewee import Model, SqliteDatabase, CharField, IntegerField

"""
This is a sample Sanic application demonstrating how to prevent SQL injection when using Peewee ORM.
"""

# Initialize the database connection
db = SqliteDatabase('example.db')

# Define a simple model
class User(Model):
    username = CharField()
    age = IntegerField()

    # Connect the table to the database
    class Meta:
        database = db

app = sanic.Sanic("Secure SQL Service")

"""
Create a route to add a new user, which is vulnerable to SQL injection.
This is for demonstration purposes only and should not be used in production.
"""
@app.route('/add_user', methods=['POST'])
def vulnerable_add_user(request):
    username = request.json.get('username')
    age = request.json.get('age')
    try:
        # This is vulnerable to SQL injection!
        query = f"INSERT INTO users (username, age) VALUES ('{username}', {age})"
        with db.execution_context():
            db.execute_sql(query)
        return json({'message': 'User added successfully'})
    except Exception as e:
        return json({'error': str(e)})

"""
Create a route to add a new user, which is secure against SQL injection.
This uses Peewee's ORM to prevent SQL injection.
"""
@app.route('/secure_add_user', methods=['POST'])
def secure_add_user(request):
    username = request.json.get('username')
    age = request.json.get('age')
    try:
        # This is safe from SQL injection since Peewee ORM is used
        user = User.create(username=username, age=age)
        return json({'message': 'User added securely', 'user_id': user.id})
    except Exception as e:
        return json({'error': str(e)})

if __name__ == '__main__':
    # Create the table before running the application
    db.create_tables([User])
    app.run(host='0.0.0.0', port=8000, debug=True)