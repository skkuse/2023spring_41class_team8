from django.urls import path
from . import views

urlpatterns = [
    path("user", views.register_view, name="register_view"),
    path("user/login", views.register_view, name='login_view'),
    path("user/idcheck", views.user_idcheck, name='user_idcheck')
    # 다른 URL 패턴들
    # ...
]
