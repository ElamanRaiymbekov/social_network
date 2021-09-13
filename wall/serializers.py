from rest_framework import serializers
from comments.serializers import RecursiveSerializer, FilterCommentListSerializer
from .models import Post, Comment, Like, Rating


class CreateCommentSerializer(serializers.ModelSerializer):
    """ Добавление комментариев к посту"""
    class Meta:
        model = Comment
        fields = ("post", "text", "parent")


class ListCommentSerializer(serializers.ModelSerializer):
    """ Список комментариев"""
    text = serializers.SerializerMethodField()
    children = RecursiveSerializer(many=True)
    user = serializers.ReadOnlyField(source='user.username')

    def get_text(self, obj):
        if obj.deleted:
            return None
        return obj.text

    class Meta:
        list_serializer_class = FilterCommentListSerializer
        model = Comment
        fields = ("id", "post", "user", "text", "created_date", "update_date", "deleted", "children")


class PostSerializer(serializers.ModelSerializer):
    """ Вывод и редактирование поста"""
    user = serializers.ReadOnlyField(source='user.username')
    comments = ListCommentSerializer(many=True, read_only=True)
    view_count = serializers.CharField(read_only=True)

    class Meta:
        model = Post
        fields = ("id", "create_date", "user", "text", "comments", "view_count")


class ListPostSerializer(serializers.ModelSerializer):
    """ Список постов"""
    user = serializers.ReadOnlyField(source='user.username')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes'] = instance.likes.filter(like=True).count()
        return representation

    class Meta:
        model = Post
        fields = ("id", "create_date", "user", "text", "likes")


class LikeSerializer(serializers.ModelSerializer):
    """Лайки"""
    class Meta:
        model = Like
        fields = ('user', 'post', 'like')


class RatingSerializer(serializers.ModelSerializer):
    """Рейтинг"""
    class Meta:
        model = Rating
        fields = ('user', 'post', 'rating')
