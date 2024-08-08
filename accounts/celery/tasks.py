from celery import shared_task
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
import time
import logging
from accounts.models import Accounts

logging.basicConfig(level=logging.ERROR)

class SeleniumUpdater:
    driver = None

    def __init__(self):
        self.init_driver()

    def init_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        self.driver = webdriver.Chrome(options=options)

    def open(self, url):
        self.driver.get(url)

    def add_cookies(self, cookies):
        for cookie in cookies:
            self.driver.add_cookie(cookie)

    def update_account(self, account):
        self.open('https://www.wildberries.ru')

        cookies = json.loads(account.cookies)
        self.add_cookies(cookies)
        self.driver.refresh()
        time.sleep(5)

        new_cookies = self.driver.get_cookies()
        new_token = self.driver.execute_script("return window.localStorage.getItem('wbx__tokenData');")

        account.cookies = json.dumps(new_cookies)
        account.token = new_token
        account.save()

    def quit(self):
        if self.driver:
            self.driver.quit()

@shared_task
def update_tokens():
    updater = SeleniumUpdater()
    accounts = Accounts.objects.all()
    for account in accounts:
        try:
            updater.update_account(account)
        except Exception as e:
            logging.error(f"Error updating account {account.id}: {e}")
    updater.quit()
