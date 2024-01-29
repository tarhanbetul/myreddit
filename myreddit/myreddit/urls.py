from django.urls import path, include
from rest_framework.routers import DefaultRouter
from myapp.views import PostViewSet, RegisterView, CustomTokenObtainPairView, CommentViewSet
from myapp.views import UserUpdateView
from django.conf import settings
from django.conf.urls.static import static
from myapp.views import UserProfileView, UserListView
from django.contrib import admin
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/posts/<int:post_id>/comments/', CommentViewSet.as_view({'post_pk': 'post_pk'}), name='post-comments'),

    path('', include('myapp.urls')),  # myapp.urls, projenizdeki ana uygulama URL'larına yönlendirir
    path('admin/', admin.site.urls),
    path('api/users/', UserListView.as_view(), name='user-list'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/user/update/', UserUpdateView.as_view(), name='user-update'),
    path('api/user/<int:pk>/', UserProfileView.as_view(), name='user-profile'),
]
# Medya dosyalarını servis etmek için bu ayarı ekleyin
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)