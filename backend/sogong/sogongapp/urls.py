from django.urls import path
from . import views

urlpatterns = [
    path("user", views.register_view, name="register_view"),
    path("user/login", views.register_view, name='login_view'),
    path("user", views.userinfo_view, name='userinfo_view'),
    path("user", views.user_newinfo, name='user_newinfo'),
    path("ethics", views.ethics_view, name='ethics_view'),
    path("ethics/submission", views.ethics_submission, name='ethics_submission'),
    path("codings", views.codings_view, name='codings_view'),
    path("codings/answer", views.coding_answer, name='coding_answer'),
    path("codings/submission", views.useranswer_view, name='useranswer_view'),
    # 다른 URL 패턴들
    # ...
]
