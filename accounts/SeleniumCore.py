import typing
from seleniumwire import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import random
from constants import DEBUG

class NotFoundInputException(Exception):
    pass


class Selenium:
    driver: WebDriver = None

    def __init__(self):
        self.init_driver()

    def init_driver(self):
        proxy_info = random.choice()
        proxy = proxy_info['proxy']
        login = proxy_info['login']
        password = proxy_info['password']

        options = webdriver.ChromeOptions()
        seleniumwire_options = {
            'proxy': {
                'https': f'socks5://{login}:{password}@{proxy}',
                'verify_ssl': False,
            },
        }

        ua = UserAgent()
        user_agent = ua.random
        options.add_argument(f"user-agent={user_agent}")
        if not DEBUG:
            options.add_argument("headless")

        self.driver = webdriver.Chrome(
            options=options,
            seleniumwire_options=seleniumwire_options
        )

    def open(self, url: str):
        self.driver.get(url)

    def has_elements(self, selector: str) -> bool:
        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
        return len(elements) > 0

    def add_cookies(self, cookies: typing.List[dict]):
        for cookie in cookies:
            self.driver.add_cookie(cookie)

    def set_session(self, session_id: str):
        if self.driver:
            self.driver.close()
        self.init_driver()
        self.driver.session_id = session_id

    def get_cookies(self):
        return self.driver.get_cookies()

    def set_token(self, token: str):
        self.driver.request_interceptor = lambda request: request.headers.update({'Authorization': f'Bearer {token}'})

    def get_elements(self, selector: str, error_text: str = "No elements found") -> typing.List[WebElement]:
        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
        if not elements:
            raise NotFoundInputException(error_text)
        return elements

    def get_element(self, selector: str, error_text: str = "Element not found") -> WebElement:
        return self.get_elements(selector, error_text)[0]

    def __del__(self):
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                print(f"Error while quitting the driver: {e}")
