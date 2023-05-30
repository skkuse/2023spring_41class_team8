from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    # 다른 URL 패턴들
    # ...
]
