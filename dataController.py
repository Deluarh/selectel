import json
import sqlite3


def db_conn():
    return sqlite3.connect("tickets.db")


def collector_ticket(tuples):
    themes = []
    for (status, link, time, id_ticket, tickets_text, notification) in tuples:
        themes.append({'ticket_status': status, 'ticket_link': link,
                       'ticket_date': time, 'ticket_id': id_ticket,
                       'ticket_text': tickets_text, 'notification': notification})
    return themes


def get_ticket_list():
    with db_conn() as db:
        tuples = db.execute("SELECT * FROM tickets ORDER BY time DESC")
        return collector_ticket(tuples)


def get_sent_tickets():
    with db_conn() as db:
        tuples = db.execute("SELECT * FROM tickets WHERE notification > 0")
        return collector_ticket(tuples)


def clear_table():
    with db_conn() as db:
        db.execute("DELETE FROM tickets;")

def write_tickets(tickets_list):
    tickets_format = []
    for data in tickets_list:
        status = data['ticket_status']
        link = data['ticket_link']
        time = data['ticket_date']
        id = data['ticket_id']
        text = data['ticket_text']
        notification = data['notification']

        tickets_format.append((status, link, time, id, text, notification))

    with db_conn() as db:
        db.executemany("INSERT INTO tickets VALUES (?,?,?,?,?,?)", tickets_format)


def create_table():
    with db_conn() as db:
        db.execute("""CREATE TABLE tickets
                     (status text, link text, time text,
                       id_ticket text,tickets_text text, notification text)
                  """)

def check_ticket(time, id):
    with db_conn() as db:
        tuples = db.execute(f'SELECT * FROM tickets WHERE time={time} and id_ticket={id};')
        return collector_ticket(tuples)

if __name__ == "__main__":
    for ticket in get_sent_tickets():
        print((ticket['ticket_date'], ticket['ticket_id']))
    print(check_ticket(1589443080.0, 1120447))
