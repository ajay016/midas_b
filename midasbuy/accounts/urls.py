from django.urls import path
from . import views

urlpatterns = [
    path("",                        views.account_list,          name="account_list"),
    path("add/",                    views.account_add,           name="account_add"),
    path("<int:pk>/delete/",        views.account_delete,        name="account_delete"),
    path("<int:pk>/login/",         views.account_login,         name="account_login"),
    path("<int:pk>/status/",        views.account_session_status,name="account_status"),
]
