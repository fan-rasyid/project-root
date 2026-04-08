import requests

# Function to fetch all customers with pagination
def fetch_all_customers(base_url):
    page = 1 
    limit = 10
    all_data = []

    while True:
        res = requests.get(f"{base_url}/api/customers?page={page}&limit={limit}")
        json_data = res.json()

        data = json_data["data"]
        if not data:
            break

        all_data.extend(data)

        if len(all_data) >= json_data["total"]:
            break

        page += 1

    return all_data