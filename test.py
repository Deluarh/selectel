import json
data = None
with open("pass.json", "r") as read_file:
    data = json.load(read_file)
username = data['mail_username']
password = data['mail_password']
print(username)
print(password)
