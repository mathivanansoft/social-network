from django.urls import path

from rest_framework.authtoken import views

from .views import ListUserAPIView, SignupAPIView

urlpatterns = [
    path('login/', views.obtain_auth_token),
    path("users/", ListUserAPIView.as_view()),
    path("signup/", SignupAPIView.as_view()),

]
