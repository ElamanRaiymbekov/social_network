from django.urls import path
from .views import *

urlpatterns = [
    path('<int:pk>', FollowerView.as_view()),
    path('', ListFollowerView.as_view())
]
