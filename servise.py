import requests
import json
from flask import Flask, request

from mail import login
from parser import ticketsParser

app = Flask(__name__)


@app.route('/send_email', methods=['POST'])
def send_mail():
    """
        JSON {"mail": str, "text": str}
        :return: {'OK': bool}
        """
    mail = request.json["mail"]
    text = request.json["text"]
    try:
        sender(mail, text, False)
    except Exception as e:
        print(e)
        return {'OK': False}
    else:
        return {'OK': True}


@app.route('/parser', methods=['POST'])
def parser():
    global driver
    driver.automatically_send_data()



@app.route('/control_servise', methods=['POST'])
def control_servise():
    """
       JSON {"mail": bool, "parser": bool}
       :return: {'OK': bool}
       """
    global driver
    global sender
    mail = request.json["mail"]
    parser = request.json["parser"]
    if parser:
        driver = ticketsParser()
        driver.auth(client_login, client_password)
    else:
        try:
            driver.close()
        except Exception as e:
            pass

    if mail:
        sender = login(username, password)


driver = None
sender = None

if __name__ == "__main__":
    driver = None
    data = None
    with open("pass.json", "r") as read_file:
        data = json.load(read_file)
    username = data['mail_username']
    password = data['mail_password']

    client_login = data['selectel_login']
    client_password = data['selectel_password']
    try:
        app.run(port=3000)
    except Exception as e:
        print(e)
