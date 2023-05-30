from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("user/login/", views.userinfo_view, name='userinfo_view')
    # 다른 URL 패턴들
    # ...
]
