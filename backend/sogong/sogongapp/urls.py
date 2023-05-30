from django.urls import path
from . import views

urlpatterns = [
    path("register", views.register_view, name="register_view"),
    path("user/idcheck", views.user_idcheck, name="user_idcheck"),
    path("user", views.login_view, name='login_view'),
    path("ethics", views.ethics_view, name='ethics_view'),
    path("ethics/submission", views.ethics_submission, name='ethics_submission'),
    path("codings", views.codings_view, name='codings_view'),
    path("codings/answer", views.coding_answer, name='coding_answer'),
    path("codings/submission", views.useranswer_view, name='useranswer_view'),
]
