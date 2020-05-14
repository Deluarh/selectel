import json
import datetime as DT
import requests
from flask import Flask, request
from mail import login
from parser import ticketsParser

app = Flask(__name__)


def data_to_str(data):
    status = data['ticket_status']
    link = data['ticket_link']
    text = data['ticket_text']
    time = DT.datetime.fromtimestamp(data['ticket_date']).strftime('%d.%m.%Y %H:%M')
    id = data['ticket_id']
    return f'статус тикета: {status} <br> ссылка на тикет: {link} <br> текст тикета:  {text} <br>  время тикета:  {time} <br>  id тикета: {id}'


def calc_desired_ticket(data, index=-2):
    sort = [(i, int(data[i]['ticket_date'])) for i in range(0, len(data))]
    sort.sort(key=lambda i: i[1])
    return data[sort[index][0]]


def last_ticket():
    templates = []
    with open('data.json') as f:
        templates = json.loads(f.read())
        print(templates)
        return calc_desired_ticket(templates, -2)


form = '''<br><br><form action="/send" method="post">
    <label for="say">отправка почты на адрес:</label>
    <input name="mail"  value="mail получателя тикета">
    <button>отправить</button>
</form><br><br><a href="/update">обновить тикеты</a>'''


@app.route("/")
def show_ticket():
    return data_to_str(last_ticket()) + form


@app.route('/send', methods=['POST'])
def send_email(text=data_to_str(last_ticket())):
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
    return {'OK': driver.automatically_send_data()}


if __name__ == "__main__":
    data = None
    with open("pass.json", "r") as read_file:
        data = json.load(read_file)
    username = data['mail_username']
    password = data['mail_password']

    client_login = data['selectel_login']
    client_password = data['selectel_password']
    try:
        driver = ticketsParser()
        driver.auth(client_login, client_password)
        sender = login(username, password)
        app.run()
    except Exception as e:
        print(e)
