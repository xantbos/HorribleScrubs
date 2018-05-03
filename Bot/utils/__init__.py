import json

# Our setup file
with open('../setup.json', encoding="utf8") as file:
    setup_file = json.load(file)

# Our user agent
user_agent = "HorribleScrubs"