import logging

from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt

from .models import Accounts
from .main import generic
logging.basicConfig(level=logging.error)


@csrf_exempt
def main(request: HttpRequest) -> HttpResponse:
    data = {}
    if request.method == "POST":
        count = int(request.POST.get("count"))
        sex = request.POST.get("sex")
        success = 0
        for _ in range(count):
            try:
                login = "3AyjX5"
                password = "7UdKL7vKQyQ7"
                proxy = "95.165.137.114:1632"
                profile = generic(sex, proxy, login, password)
                Accounts(
                    session=profile.session,
                    phone_number=profile.phone_number,
                    sex=sex,
                    first_name=profile.name,
                    last_name=profile.surname,
                    cookies=profile.cookie,
                    token=profile.token,
                ).save()
                success += 1
            except Exception as e:
                logging.error(f"Error creating account: {e}")
        data["success"] = success
    return render(request, "main.html", data)
