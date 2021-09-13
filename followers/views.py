from rest_framework import generics, permissions, views, response
from users.models import User
from .models import Followers
from .serializers import UserProfileSerializer


class ListFollowerView(generics.ListAPIView):
    """Вывод подписчиков пользователя"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return Followers.objects.filter(user=self.request.user)


class FollowerView(views.APIView):
    """ Добавление в подписчики
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except Followers.DoesNotExist:
            return response.Response(status=404)
        Followers.objects.create(subscriber=request.user, user=user)
        return response.Response('Вы успешно подписались на пользователя.', status=201)

    def delete(self, request, pk):
        try:
            sub = Followers.objects.get(subscriber=request.user, user_id=pk)
        except Followers.DoesNotExist:
            return response.Response(status=404)
        sub.delete()
        return response.Response('Вы успешно отписались от пользователяю.', status=204)
