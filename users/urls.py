from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import *

router = DefaultRouter()

router.register('', UserProfileViewSet)

urlpatterns = [
    path('get/', include(router.urls)),

    path('register/', RegistrationView.as_view()),
    path('activation/', ActivationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
    path('forgot_password/', ForgotPasswordView.as_view()),
    path('forgot_password_complete/', ForgotPasswordCompletedView.as_view())

]
