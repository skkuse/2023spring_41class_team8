from django.urls import path
from . import views

urlpatterns = [
    path("user", views.register_view, name="register_view"),
    path("user/login/", views.register_view, name='login_view'),
    path("user", views.userinfo_view, name='userinfo')
    # 다른 URL 패턴들
    # ...
]
