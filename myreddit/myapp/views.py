from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from myapp.serializers import CommentSerializer
from .serializers import CustomUserSerializer
from rest_framework import generics
from myapp.models import Comment
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, Post, Activity, Comment
from .serializers import UserProfileSerializer, CommentSerializer
from datetime import timedelta
from django.shortcuts import render, get_object_or_404

def index(request):
    return render(request, 'index.html')  # varsayılan olarak templates dizininde bir index.html dosyası kullanılır

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        # perform_create, bir nesne (gönderi) kaydedilirken çağrılır ve
        # burada ek alanları elle doldurabilirsiniz.
        serializer.save(created_by=self.request.user)

class UserListView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):

        post_id = self.kwargs.get('post_pk')
        queryset = Comment.objects.filter(post__id=post_id)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_pk')
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(created_by=self.request.user, post=post)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        # Bu, güncellenen kullanıcının detaylarını almak için kullanılır
        return self.request.user

class UserProfileView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

#
# class CustomTokenObtainPairView(TokenObtainPairView):
#     def post(self, request, *args, **kwargs):
#
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.user
#             remember_me = request.data.get('remember_me', False)
#
#             refresh = RefreshToken.for_user(user)
#
#             if not remember_me:
#                 refresh.access_token.lifetime = timedelta(minutes=15)  # Örnek olarak 15 dakika
#
#             data = {
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             }
#             return Response(data, status=status.HTTP_200_OK)
#
#         return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)