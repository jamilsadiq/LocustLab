import json
import os

def load_json_payload(filename):
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, 'payloads', filename)

    with open(file_path, 'r') as file:
        return json.load(file)

