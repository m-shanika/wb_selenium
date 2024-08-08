from urllib3.exceptions import MaxRetryError

from .FakeData import FakeData
from .smsActivate import SMSActivate
from .RuCaptcha import RuCaptcha
from .SeleniumCore import Selenium, NotFoundInputException
import time
from .statuses import Profile, Sex
from constants import RUCAPTCHA_KEY, SMS_ACTIVATE_KEY, PROXY
from .utils import convert_sex_to_gender
import json
import logging

logging.basicConfig(level=logging.INFO)


def generic(sex: Sex):
    sel = Selenium(PROXY)
    sel.driver.start_session({})
    sms_activate = SMSActivate(SMS_ACTIVATE_KEY)
    sel.open("https://www.wildberries.ru/security/login")
    time.sleep(5)

    phone_element = sel.get_element("input[type='text'][inputmode='tel'].input-item", "not found phone input")
    phone_element.clear()

    phone_info = sms_activate.get_number()
    phone_number = phone_info['phoneNumber']
    id = phone_info['activationId']

    phone_element.send_keys(phone_number)
    request_code_button = sel.get_element("#requestCode", "Not found request code button")
    request_code_button.click()
    time.sleep(3)

    def solve_captcha():
        captcha_element = sel.get_element("img.form-block__captcha-img", "Not found image captcha")
        captcha_input_element = sel.get_element("#smsCaptchaCode", "Not found captcha input")
        captcha_input_element.clear()
        image_name = "img.jpg"
        RuCaptcha.save_image(image_name, captcha_element.get_attribute("src"))
        answer = RuCaptcha.solve_captcha(RUCAPTCHA_KEY, image_name)
        if answer.error:
            raise Exception("Can't solve the captcha")
        captcha_input_element.send_keys(answer.captchaSolve.upper())
        time.sleep(5)
        if sel.get_element("#smsCaptchaCode", "Not found captcha input"):
            return solve_captcha()

    for attempt in range(3):
        try:
            solve_captcha()
            break
        except NotFoundInputException as e:
            print(e)
        except MaxRetryError as e:
            print(e)
        except Exception as e:
            print(e)
            if attempt == 2:
                raise e
            else:
                time.sleep(2)

    try:
        code = sms_activate.wait_for_sms(id)
        for i in range(6):
            try:
                elements_to_input = sel.get_elements("input.char-input__item.j-b-charinput", "Not found input code")
                elements_to_input[i].clear()
                elements_to_input[i].send_keys(code[i])
            except NotFoundInputException as e:
                print('Not found input code', e)
                time.sleep(2)

        sms_activate.set_status(id, 6) 
    except TimeoutError as e:
        sms_activate.set_status(id, 8)  
        raise Exception("Failed to receive SMS within the timeout period") from e

    fake_data = FakeData.get(convert_sex_to_gender(sex))

    sel.open("https://www.wildberries.ru/lk/details")
    time.sleep(5)
    try:
        personal_name_button = sel.get_element("button.personal-data__edit", "Not found name button")
        personal_name_button.click()
        time.sleep(5)
        input_fio = sel.get_element("#Item\.FirstName", "Not found name input")
        input_fio.clear()
        input_fio.send_keys(f"{fake_data.LastName} {fake_data.FirstName}")
        button_save = sel.get_element("button.btn-main", "Not found save button")
        button_save.click()
    except Exception as e:
        print('exception occured when filling name')
    try:
        sex_radio_button = sel.get_elements("label.personal-data__radio")
        if sex == Sex.MALE:
            sex_radio_button[0].click()
        else:
            sex_radio_button[1].click()
    except Exception as e:
        print('exception occured when changing sex')
    token = ""
    local_storage = sel.driver.execute_script("return window.localStorage;")
    for key in local_storage:
        if key == "wbx__tokenData":
            token_data = json.loads(local_storage[key])
            token = token_data['token']
            break

    all_cookies = sel.get_cookies()
    cookies_dict = {}
    for cookie in all_cookies:
        cookies_dict[cookie['name']] = cookie['value']
    print(cookies_dict)

    profile = Profile(
        surname=fake_data.LastName,
        name=fake_data.FirstName,
        session=str(sel.driver.session_id),
        phone_number=phone_number,
        sex=sex,
        cookie=json.dumps(sel.driver.get_cookies()),  
        token=token
    )

    return profile
