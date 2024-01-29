# myapp/views.py
# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Örnek bir URL pattern'ı
    # Buraya diğer URL pattern'larınızı ekleyebilirsiniz
]
