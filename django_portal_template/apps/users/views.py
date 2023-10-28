from axes.models import AccessLog
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.gis.geoip2 import GeoIP2
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView, RedirectView
from django_otp.plugins.otp_static.models import StaticDevice
from django_otp.plugins.otp_totp.models import TOTPDevice

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"


user_detail_view = UserDetailView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


user_redirect_view = UserRedirectView.as_view()


@login_required
def user_settings_view(request):
    """
    User settings page. Collates all user and account view links into a single user page.
    Also displays an access log.
    """
    user = request.user
    totp_dev = TOTPDevice.objects.devices_for_user(user, confirmed=True)
    static_dev = StaticDevice.objects.devices_for_user(user, confirmed=True)

    g = GeoIP2()
    access_history = []
    for log in AccessLog.objects.filter(username=user).order_by("-attempt_time")[:30]:
        try:
            geo_ip = g.city(log.ip_address)
            access_history.append(
                {
                    "device": log.user_agent,
                    "location": str(geo_ip["city"]) + ", " + str(geo_ip["country_name"]),
                    "ip_address": log.ip_address,
                    "time": log.attempt_time,
                }
            )
        except Exception:
            access_history.append(
                {
                    "device": log.user_agent,
                    "location": "Unknown",
                    "ip_address": log.ip_address,
                    "time": log.attempt_time,
                }
            )

    return render(
        request,
        "users/user_settings_page.html",
        {
            "totp_dev": totp_dev,
            "static_dev": static_dev,
            "access_history": access_history,
        },
    )
