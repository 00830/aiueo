from django.urls import path
from . import views

app_name = "app1"

urlpatterns = [
    path('search/', views.Search.as_view(), name='main'),
    path('login/', views.Login.as_view(), name='login'),
    path('login/register/', views.Register.as_view(), name='registerUser'),
    path('login/register/confirm/', views.RegisterConfirm.as_view(), name='registerUserConfirm'),
    path('login/register/commit/', views.RegisterComplete.as_view(), name='registerUserCommit'),
]