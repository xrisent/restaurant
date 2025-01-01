from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from . import views
from .views import UploadPhotoView

router = DefaultRouter()
router.register(r'person', views.PersonViewSet)
router.register(r'user', views.UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('current_user/', views.CurrentUserView.as_view(), name='current_user'),
    path('person/<int:pk>/upload_photo/', UploadPhotoView.as_view(), name='upload-photo'),

    # JWT tokens
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
