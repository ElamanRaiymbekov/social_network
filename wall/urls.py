from django.urls import path
from .views import *


urlpatterns = [
    path('comment', CommentsView.as_view({'post': 'create'})),
    path('comment/<int:pk>', CommentsView.as_view({'put': 'update', 'delete': 'destroy'})),
    path('post', PostView.as_view({'post': 'create'})),
    path('post/<int:pk>', PostView.as_view({
        'get': 'retrieve', 'put': 'update', 'delete': 'destroy'
    })),
    path('<int:pk>', PostListView.as_view()),
    path('like/<int:pk>', LikeView.as_view()),
    path('rating/<int:pk>', RatingView.as_view()),

]
