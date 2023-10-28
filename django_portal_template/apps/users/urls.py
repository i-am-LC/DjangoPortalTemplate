from django.urls import path

from django_portal_template.apps.users.views import user_detail_view, user_redirect_view, user_settings_view

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("<int:pk>/", view=user_detail_view, name="detail"),
    path("settings/", view=user_settings_view, name="user_settings_view"),
]
