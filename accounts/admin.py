from django.contrib import admin
from .models import Accounts

@admin.register(Accounts)
class AccountsAdmin(admin.ModelAdmin):
    list_display = [
        "id", "session", "phone_number", "sex", "first_name", "last_name", "is_buy"
    ]

