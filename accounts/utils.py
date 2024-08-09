from accounts.models import Accounts
from .dataclasses import Sex, FDGender

def convert_sex_to_gender(sex: Sex):
    if sex == Sex.MALE:
        return FDGender.MAN
    elif sex == Sex.FEMALE:
        return FDGender.WOMAN
    else:
        return FDGender.UNSET

import json

def load_account_cookies_and_session(account_id):
    account = Accounts.objects.get(id=account_id)
    try:
        cookies = json.loads(account.cookies)  
    except json.JSONDecodeError as e:
        print(f"Ошибка при декодировании JSON: {e}")
        print(f"Неверные куки: {account.cookies}")
        raise
    session_id = account.session
    return cookies, session_id


