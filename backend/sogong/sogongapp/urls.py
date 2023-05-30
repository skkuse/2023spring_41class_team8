from django.urls import path
from . import views

urlpatterns = [
    path("user", views.register_view, name="register_view"),
    path("user/login", views.register_view, name='login_view'),
    path("user/login", views.userinfo_view, name='userinfo_view'),
    path("user/login", views.ethics_view, name='ethics_view'),
    path("user/login", views.ethics_submission, name='ethics_submission'),
    path("user/login", views.codings_view, name='codings_view'),
    path("user/login", views.coding_answer, name='coding_answer'),
    path("user/login", views.useranswer_view, name='useranswer_view'),
    # 다른 URL 패턴들
    # ...
]
