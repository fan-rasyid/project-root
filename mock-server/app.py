from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

# Load data from JSON file
DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "customer.json")
def load_data():
    with open(DATA_FILE) as f:
        return json.load(f)
    
# Health check endpoint    
@app.route('/api/health')
def health():
    return {"status":"ok"}

# Endpoint to get customer with pagination and limit from JSON file
@app.route('/api/customers')
def get_customers():
    data = load_data()

    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))

    start = (page - 1) * limit
    end = start + limit

    return jsonify({
        "data" : data[start:end],
        "total" : len(data),
        "page": page,
        "limit": limit
    })

# Endpoint to get customer by ID from JSON file
@app.route('/api/customers/<customer_id>')
def get_customer(customer_id):
    data = load_data()
    customer = next((c for c in data if c["customer_id"] == customer_id), None)

    if not customer:
        return jsonify({"error" : "Customer not found"}, 404)

    return customer

# Run the Flask app
if __name__ == '__main__':
    app.run(
        host="0.0.0.0", 
        port=5000,
    )