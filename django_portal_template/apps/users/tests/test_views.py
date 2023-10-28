from unittest.mock import Mock, patch

import pytest
from axes.models import AccessLog
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseRedirect
from django.test import RequestFactory
from django.urls import reverse

from django_portal_template.apps.users.models import User
from django_portal_template.apps.users.tests.factories import UserFactory
from django_portal_template.apps.users.views import UserRedirectView, user_detail_view, user_settings_view

pytestmark = pytest.mark.django_db


class TestUserRedirectView:
    def test_get_redirect_url(self, user: User, rf: RequestFactory):
        view = UserRedirectView()
        request = rf.get("/fake-url")
        request.user = user

        view.request = request
        assert view.get_redirect_url() == f"/users/{user.pk}/"


class TestUserDetailView:
    def test_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = UserFactory()
        response = user_detail_view(request, pk=user.pk)

        assert response.status_code == 200

    def test_not_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = AnonymousUser()
        response = user_detail_view(request, pk=user.pk)
        login_url = reverse(settings.LOGIN_URL)

        assert isinstance(response, HttpResponseRedirect)
        assert response.status_code == 302
        assert response.url == f"{login_url}?next=/fake-url/"


class TestUserSettingsView:
    def test_user_settings_view_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get(reverse("users:user_settings_view"))
        request.user = user
        response = user_settings_view(request)

        assert response.status_code == 200

    def test_user_settings_view_not_authenticated(self, rf: RequestFactory):
        request = rf.get(reverse("users:user_settings_view"))
        request.user = AnonymousUser()
        response = user_settings_view(request)

        assert response.status_code == 302
        assert response.url == reverse("account_login") + "?next=" + reverse("users:user_settings_view")

    def test_user_settings_view_access_history(self, user: User, rf: RequestFactory):
        # Create a mock GeoIP2 object
        geoip_mock = Mock()
        geoip_mock.city.return_value = {"country_name": "Unknown", "region_name": "Unknown", "city": "Unknown"}

        # Create a request object
        request = rf.get(reverse("users:user_settings_view"))
        request.user = user

        # Call the view function with the mock GeoIP2 object
        with patch("django_portal_template.apps.users.views.GeoIP2", return_value=geoip_mock):
            response = user_settings_view(request)

        # Assert the response
        assert response.status_code == 200

        # Create an AccessLog object
        AccessLog.objects.create(username=user, ip_address="127.0.0.1", user_agent="Test User Agent")

        # Call the view function again with the mock GeoIP2 object
        with patch("django_portal_template.apps.users.views.GeoIP2", return_value=geoip_mock):
            response = user_settings_view(request)

        # Assert the response
        assert response.status_code == 200
