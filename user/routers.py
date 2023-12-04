from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [

    # Define a custom URL pattern for change_password.
    path('users/<int:pk>/change_password/', UserViewSet.as_view({'post': 'change_password'}), name='user-change-password'),
]

urlpatterns += router.urls
