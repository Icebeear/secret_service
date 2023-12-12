from django.urls import path
from .views import SecretCreateAPIView, SecretRetrieveAPIview

urlpatterns = [
    path('generate/', SecretCreateAPIView.as_view(), name='generate_secret'),
    path('secrets/<str:secret_key>/', SecretRetrieveAPIview.as_view(), name='reveal_secret'),
]
