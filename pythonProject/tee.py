DB_CONFIG = {'host': 'localhost', 'user': 'root', 'password': '42a'}

DB_CONFIG = {'host': 'localhost', 'user': 'root', 'password': '42a'}

for key, value in DB_CONFIG.items():
    print(f"{key}: {value}")
    if value is None or value == "":
        print(f"Error: {key} has an invalid value: {value}")