from flask import Flask, request, jsonify

app = Flask(__name__)

users = {
    1: {"name": "Alice", "city": "London"},
    2: {"name": "Bob", "city": "Paris"}
}
next_user_id = 3 

# GET used to read data
@app.route('/users', methods=['GET'])
def get_all_users():
    """Returns a list of all users."""
    
    user_list = [{"id": uid, **data} for uid, data in users.items()]
    return jsonify(user_list)

# GET used to read one by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Returns a specific user by ID."""
    user_data = users.get(user_id)
    if user_data:
        return jsonify({"id": user_id, **user_data})
    return jsonify({"message": f"User with ID {user_id} not found"}), 404


# POST used to add new data
@app.route('/users', methods=['POST'])
def create_user():
    """Creates a new user from JSON data."""
    global next_user_id
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"message": "Missing 'name' in request body"}), 400

    new_user = {
        "name": data['name'],
        "city": data.get('city', 'Unknown') 
    }

    # Storing the new data and increment the ID automatic
    users[next_user_id] = new_user
    created_id = next_user_id
    next_user_id += 1
    return jsonify({"id": created_id, **new_user}), 201

# PUT Modify an existing data
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates an existing user's data."""
    if user_id not in users:
        return jsonify({"message": f"User with ID {user_id} not found"}), 404

    data = request.get_json()
    if 'name' in data:
        users[user_id]['name'] = data['name']
    if 'city' in data:
        users[user_id]['city'] = data['city']
    return jsonify({"id": user_id, **users[user_id]})

# DELETE Remove data
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a specific user by ID."""
    if user_id in users:
        del users[user_id]
        return '', 204
    return jsonify({"message": f"User with ID {user_id} not found"}), 404
#Run the App
if __name__ == '__main__':
    app.run(debug=True)