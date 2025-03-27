from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# In-memory "database" for items
items = [
    {"id": 1, "name": "Item One", "description": "The first item"},
    {"id": 2, "name": "Item Two", "description": "The second item"}
]

def find_item(item_id):
    return next((item for item in items if item["id"] == item_id), None)

# Retrieve all items
@app.route("/items", methods=["GET"])
def get_items():
    return jsonify(items), 200

# Retrieve a single item by id
@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = find_item(item_id)
    if item:
        return jsonify(item), 200
    abort(404, description="Item not found")

# Create a new item
@app.route("/items", methods=["POST"])
def create_item():
    new_item = request.get_json()
    if not new_item or "name" not in new_item or "description" not in new_item:
        abort(400, description="Invalid request payload")
    new_item["id"] = max(item["id"] for item in items) + 1 if items else 1
    items.append(new_item)
    return jsonify(new_item), 201

# Update an existing item
@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    item = find_item(item_id)
    if not item:
        abort(404, description="Item not found")
    update_data = request.get_json()
    if not update_data:
        abort(400, description="Invalid request payload")
    item.update(update_data)
    return jsonify(item), 200

# Delete an item
@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = find_item(item_id)
    if not item:
        abort(404, description="Item not found")
    items.remove(item)
    return jsonify({"message": "Item deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)