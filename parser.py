import time
import sys
import json
import datetime

import bs4
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, WebDriverException

class ticketsParser():
    class Decorators(object):
        @classmethod
        def check_func(cls, func):
            def wrapped(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print("Error:", e)
                    print(e.__class__)
                    return False

            return wrapped

    def __init__(self):
        url = 'https://my.selectel.ru/tickets?type=all&page=1'
        
        CHROME_PATH = '/usr/bin/google-chrome'
        CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
        WINDOW_SIZE = "1920,1080"

        chrome_options = Options()  
        chrome_options.add_argument("--headless")  
        chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        chrome_options.binary_location = CHROME_PATH

        try:
            self.driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                                           options=chrome_options)
    
        except WebDriverException as e:
            print(e)
        except Exception as e:
            print(e)
            print(e.__class__)
        else:
            self.driver.get(url)
            print('selenium driver ok')

    @Decorators.check_func
    def auth(self, client_login, client_password):
        try: 
            print(self.driver.find_element_by_id("login"))
            login = self.driver.find_element_by_id("login")
            login.send_keys(client_login)
            login.submit()
            password = self.driver.find_element_by_id("password")
            password.send_keys(client_password)
            password.submit()
            time.sleep(3)
        except NoSuchElementException as e:
            print(e)
        else:
            return True
        return False

    @Decorators.check_func
    def extract_data(self, data):
        bs = bs4.BeautifulSoup(data, features="lxml")
        tickets = bs.find('tickets-list').find_all('tickets-item', attrs={'ticket':'ticket'})
        tickets_list = []
        for ticket in tickets:
            ticket_status = ticket.find('ticket-status').text
            ticket_link = 'https://my.selectel.ru' + ticket.div.find('div', attrs={'stl':'support_ticket_open_name'})['href']
            ticket_text = ticket.div.find('div', attrs={'stl': 'support_ticket_open_name'}).text
            ticket_id = ticket.div.find('div', attrs={'stl': 'support_ticket_open_id'}).text
            ticket_date = ticket.div.find('div', attrs={'stl': 'support_ticket_open_changed'}).text
            ticket_date = datetime.datetime.strptime(ticket_date, '%d.%m.%Y %H:%M')
            ticket_date = ticket_date.timestamp()
            tickets_list.append({'ticket_status': ticket_status, 
                                 'ticket_link': ticket_link, 
                                 'ticket_text': ticket_text,
                                 'ticket_id': ticket_id,
                                 'ticket_date': ticket_date})
        return tickets_list



    def send_data(self, data):
        with open('data.json', 'w') as f:
            f.write(json.dumps(data))
            
    def close(self):
        self.driver.quit()

    def automatically_send_data(self):
        data = self.extract_data(self.driver.page_source)
        if not data:
            self.send_data(data)
            return True
        return False


if __name__ == "__main__":
    driver = ticketsParser()
    driver.auth(sys.argv[1], sys.argv[2]) 
    time.sleep(3)
    driver.automatically_send_data()
    driver.close()
    requests.post('http://127.0.0.1:5000/send', json={'mail': sys.argv[3]})
