import json

with open('reset.json', 'r') as reset:
    default = json.load(reset)

with open('data.json', 'w') as file:
    json.dump(default, file, indent=4)