# 代码生成时间: 2025-10-13 02:18:28
import sanic
from sanic.response import json
from sanic.exceptions import ServerError

# Define the HumanResource class to manage human resources
class HumanResource:
    def __init__(self):
        self.employees = {}

    def add_employee(self, id, name, position):
        """Add a new employee to the database."""
        if id in self.employees:
            raise ValueError('Employee with the same ID already exists.')
        self.employees[id] = {'name': name, 'position': position}
        return {'id': id, 'name': name, 'position': position}

    def get_employee(self, id):
        "