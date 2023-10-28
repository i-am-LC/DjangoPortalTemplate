from __future__ import annotations

from allauth_2fa.adapter import OTPAdapter
from django.conf import settings
from django.http import HttpRequest


class AccountAdapter(OTPAdapter):
    def is_open_for_signup(self, request: HttpRequest) -> bool:
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
