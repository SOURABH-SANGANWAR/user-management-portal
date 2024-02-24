from .views import UserCreate, UserRetrieveUpdateDestroy, ForgotPassword, UserRetrive, LoginView
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('create/',UserCreate.as_view()),
    path('login/',LoginView.as_view()),
    path('forgot-password/',ForgotPassword.as_view()),
    path('user/',UserRetrieveUpdateDestroy.as_view()),
    path('user/<int:id>/',UserRetrive.as_view()),
    path('token/refresh/',TokenRefreshView.as_view()),
]