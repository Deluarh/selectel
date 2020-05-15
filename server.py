import json
import sqlite3
import datetime
import requests
from flask import Flask, request, Response
from mail import login
from parser import ticketsParser
import dataController

app = Flask(__name__)


def to_json(data):
    return json.dumps(data) + "\n"


def resp(code, data):
    return Response(
        status=code,
        mimetype="application/json",
        response=to_json(data)
    )




def data_to_str(data):
    status = str(data['ticket_status'])
    link = data['ticket_link']
    text = data['ticket_text']
    time = str(datetime.datetime.fromtimestamp(float(data['ticket_date'])).strftime('%d.%m.%Y %H:%M'))
    id = data['ticket_id']
    return f'<br> статус тикета: {status} <br> ссылка на тикет: {link} <br> текст тикета:  {text} <br>  время тикета:  {time} <br>  id тикета: {id}<br>'


def get_ticket(index=1):
    try:
        return data_to_str(dataController.get_ticket_list()[index])
    except IndexError:
        return f'нет тикета с порядковым номером {index + 1}'


form = '''<br><br><form action="/send" method="post">
    <label for="say">отправка почты на адрес:</label>
    <input name="mail"  value="mail получателя тикета">
    <button>отправить</button>
</form><br><br><a href="/update">обновить тикеты</a>'''


@app.route("/", methods=['GET'])
def show_ticket():
    return get_ticket() + form


@app.route('/send', methods=['POST'])
def send_email(text=get_ticket()):
    """
    JSON {"mail": str}
    :return: {'OK': bool}
    """
    print(request)
    try:
        mail = request.json["mail"]
    except TypeError as e:
        mail = request.form.get('mail')
    if not isinstance(mail, str) or len(text) == 0:
        return {'OK': False}

    try:
        sender(mail, text, False)
    except Exception as e:
        print(e)
        return {'OK': False}
    else:
        return {'OK': True}


@app.route('/update')
def update_tickers_list():
    with open("pass.json", "r") as read_file:
        data = json.load(read_file)
    client_login = data['selectel_login']
    client_password = data['selectel_password']
    driver = ticketsParser()
    if driver.auth(client_login, client_password):
        data = driver.automatically_send_data()
        driver.close()
        return {'OK': data}
    else:
        return {'не удалось авторизоваться на selectel'}


if __name__ == "__main__":
    app.run()
    '''
    data = None
    with open("pass.json", "r") as read_file:
        data = json.load(read_file)
    username = data['mail_username']
    password = data['mail_password']

    try:
        sender = login(username, password)
        app.run()
    except Exception as e:
        print(e)
'''
