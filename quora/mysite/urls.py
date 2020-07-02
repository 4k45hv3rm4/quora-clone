from django.urls import path
from mysite.views import (
    home,
    question_detail,
    create_answer,
    create_question,
    registration_view,
    login_view,
    account_view,
    users_list,
    user_detail,
    user_follow,
    logout_view,
    delete_question,
    delete_answer,
    )

urlpatterns = [

    path("home/", home, name="home"),
    path("answer/<slug>", create_answer, name="answer"),
    path("q_detail/<slug>/", question_detail, name="q_detail"),
    path("question/", create_question, name="question"),
    # path("profileUpdate/", profileUpdate, name="profileUpdate"),
    path("profile/", account_view, name="profile"),
    path("registration/", registration_view, name="registration"),
    path("login/", login_view, name="login"),
    path("all_users/", users_list, name="u_list"),
    path("users/follow/", user_follow, name="user_follow"),
    path("user_detail/<username>/",user_detail,name="user_detail"),

    path("logout/", logout_view, name="logout"),
    path("delete_question/<slug>", delete_question, name="delete_question"),
    path("delete_answer/<slug>/<author>", delete_answer, name="delete_answer"),

]
