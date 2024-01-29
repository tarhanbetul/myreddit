from rest_framework import serializers
from .models import Post, Comment, Activity
from .models import CustomUser
from django.shortcuts import  get_object_or_404
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        password = user.set_password(validated_data['password'])
        if password:
            user.set_password(password)
        user.save()
        return user

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'full_name', 'date_of_birth', 'bio', 'profile_picture']


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['content', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'post', 'created_by', 'created_at', 'updated_at', 'likes', 'dislikes']
        read_only_fields = ['created_by', 'created_at', 'updated_at']


    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user

        # Yorumun hangi gönderiye ait olduğunu al
        post_id = self.context['view'].kwargs.get('post_pk')
        validated_data['post'] = Post.objects.get(pk=post_id)

        comment = Comment.objects.create(**validated_data)
        return comment


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_by', 'created_at', 'updated_at', 'likes', 'dislikes', 'comments']
        read_only_fields = ['created_by', 'created_at', 'updated_at']

class UserProfileSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
    activities = ActivitySerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'profile_picture', 'date_joined', 'posts', 'activities']