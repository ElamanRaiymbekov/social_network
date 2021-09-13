from rest_framework import serializers
from users.serializers import UserProfileSerializer
from .models import Followers


class UserProfileSerializer(serializers.ModelSerializer):
    subscribers = UserProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Followers
        fields = ('subscribers',)


# TODO: Настроить отображение деталей о подписчиках (аватар, username)
