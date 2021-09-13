from rest_framework import permissions, generics, views, response
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters

from main.classes import CreateUpdateDestroy, CreateRetrieveUpdateDestroy
from main.permissions import IsAuthor
from users.models import User
from .models import Post, Comment, Like, Rating
from .serializers import (PostSerializer, ListPostSerializer, CreateCommentSerializer, LikeSerializer, RatingSerializer)


class ArticleFilter(filters.FilterSet):
    publish_at = filters.DateFromToRangeFilter('created_at', 'gte')

    class Meta:
        model = Post
        fields = ('id', 'user',)


class PostListView(generics.ListAPIView):
    """ Список постов на стене пользователя"""
    serializer_class = ListPostSerializer
    queryset = Post.objects.all()

    filter_backends = [filters.DjangoFilterBackend, rest_filters.SearchFilter,
                       rest_filters.OrderingFilter]
    filterset_class = ArticleFilter

    search_fields = ['user', 'text']
    ordering_fields = ['create_date', 'user']

    def get_queryset(self):
        return Post.objects.filter(user_id=self.kwargs.get('pk')).select_related('user').prefetch_related('comments')


class PostView(CreateRetrieveUpdateDestroy):
    """ CRUD поста"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all().select_related('user').prefetch_related('comments')
    serializer_class = PostSerializer
    permission_classes_by_action = {'get': [permissions.AllowAny],
                                    'update': [IsAuthor],
                                    'destroy': [IsAuthor]}

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentsView(CreateUpdateDestroy):
    """ CRUD комментариев к записи"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CreateCommentSerializer
    permission_classes_by_action = {'update': [IsAuthor],
                                    'destroy': [IsAuthor]}

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()


class LikeView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return response.Response(status=404)
        Like.objects.create(post=post, user=request.user, like=True)
        return response.Response('Вы поставили лайк на пост.', status=201)

    def delete(self, request, pk):
        try:
            sub = Like.objects.get(user=request.user, post=pk)
        except Like.DoesNotExist:
            return response.Response(status=404)
        sub.delete()
        return response.Response('Вы убрали свой лайк.', status=201)


class RatingView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return response.Response(status=404)
        rating = request.data.get('rating')
        if Rating.objects.filter(post=post, user=request.user).exists():
            return response.Response('Вы уже ставили оценку на пост.', status=200)
        elif rating in ['1', '2', '3', '4', '5']:
            Rating.objects.create(post=post, user=request.user, rating=rating)
            return response.Response('Вы поставили оценку посту.', status=201)

        return response.Response('Рейтинг может быть от 1 до 5', status=400)

    def delete(self, request, pk):
        try:
            rate = Rating.objects.get(user=request.user, post=pk)
        except Rating.DoesNotExist:
            return response.Response(status=404)
        rate.delete()
        return response.Response('Вы удалили оценку с поста.', status=201)

    def put(self, request, pk):
        rating = request.data.get('rating')
        if rating in ['1', '2', '3', '4', '5']:
            try:
                Rating.objects.filter(user=request.user, post=pk).update(rating=rating)
            except Rating.DoesNotExist:
                return response.Response(status=404)
            return response.Response('Вы изменили свою оценку.', status=201)
        return response.Response('Рейтинг может быть от 1 до 5', status=400)
