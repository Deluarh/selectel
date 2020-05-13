import smtplib
from email.mime.text import MIMEText
from email.header    import Header
import json

mail_receiver = 'markkozlov1@gmail.com'
text = "Python 3.4 rules them all!"

def login(username, password):
  server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
  server.login(username, password)

  def send_mail(mail_receiver, text, quit = True):
    SUBJECT = "задание на стажировку"

    nonlocal username
    nonlocal server

    msg = MIMEText(text, 'plain', 'utf-8')
    msg['Subject'] = Header(SUBJECT, 'utf-8')
    msg['From'] = username
    msg['To'] = mail_receiver
    server.sendmail(username, [mail_receiver], msg.as_string())
    print(2)
    if quit:
      server.quit()
      print('server mail quit')
    return True
  return send_mail

if __name__ == "__main__":
    data = None
    with open("pass.json", "r") as read_file:
        data = json.load(read_file)
    username = data['mail_username']
    password = data['mail_password']
    
    sender = login(username, password)
    sender(mail_receiver, text, False)
    sender(mail_receiver, text)