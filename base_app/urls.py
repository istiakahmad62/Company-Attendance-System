from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeTemplateView.as_view(), name="home"),
    path('login', views.LoginFormView.as_view(), name="log-in"),
    path('register', views.RegisterFormView.as_view(), name="register"),
    path('success', views.SuccessView.as_view(), name="success"),
    path('token', views.TokenView.as_view(), name="token"),
    path('verfiy/<str:auth_token>', views.VerfifyRedirectView.as_view(), name="verfiy"),
    path('login-check', views.LoginCheckRedirectView.as_view(), name="login-check"),
    path('logout', views.LogoutRedirectView.as_view(), name="logout"),
]
