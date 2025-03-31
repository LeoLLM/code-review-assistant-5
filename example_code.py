#!/usr/bin/env python3
"""
Example code with common issues for demonstration purposes
"""

# Global variables that should be constants
database_url = "mysql://user:password@localhost:3306/mydb"
api_key = "sk_test_1234567890abcdefghijklmn"

def get_user_data(id):
    # Directly using user input without validation
    query = "SELECT * FROM users WHERE id = " + str(id)
    # Simulated database connection
    print("Executing query: " + query)
    
    # Returning mock data
    return {"id": id, "name": "User " + str(id), "email": "user" + str(id) + "@example.com"}

# Unnecessarily complex function with nested loops - performance issue
def find_matching_items(list1, list2):
    result = []
    for i in range(len(list1)):
        for j in range(len(list2)):
            if list1[i] == list2[j]:
                result.append(list1[i])
                # Should break here to avoid duplicates
    return result

# Memory leak - file handle not closed
def read_log_file(filename):
    f = open(filename, "r")
    content = f.read()
    return content
    # Missing f.close()

# Commented out code - should be removed
# def old_function():
#     print("This is deprecated")
#     return None

class UserManager:
    def __init__(self):
        # Debug print statement
        print("UserManager initialized")
        self.users = {}
    
    # Function that does too many things - violates single responsibility
    def process_user(self, user_id, user_data):
        # Add user to database
        self.users[user_id] = user_data
        
        # Send welcome email
        self._send_email(user_id, "Welcome to our platform!")
        
        # Log user creation
        self._log_action(f"User {user_id} created")
        
        # Update metrics
        self._update_metrics("user_created")
        
        return True
    
    def _send_email(self, user_id, message):
        print(f"Sending email to user {user_id}: {message}")
    
    def _log_action(self, message):
        print(f"LOG: {message}")
    
    def _update_metrics(self, metric_name):
        print(f"Updating metric: {metric_name}")

# No docstring explaining what the function does
def calculate_total(items, tax_rate):
    t = 0
    # Cryptic variable names
    for i in items:
        t += i
    # Magic number - hardcoded value
    if t > 1000:
        t = t * 0.9  # 10% discount
    return t * (1 + tax_rate)

if __name__ == "__main__":
    # Test code
    users = UserManager()
    users.process_user(1, {"name": "John Doe", "email": "john@example.com"})
    
    print(get_user_data(1))
    print(find_matching_items([1, 2, 3, 4, 5], [3, 4, 5, 6, 7]))
    
    # Potential security issue: try-except block swallows all exceptions
    try:
        print(read_log_file("app.log"))
    except:
        pass  # Silent failure
    
    print(calculate_total([100, 200, 300], 0.07))