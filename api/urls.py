from django.urls import path

from api.serializer import LoginSerializer
from api.views import UploadAndProcessFileAPI, ASMRegisterAPI, LoginView, LogoutView
from asm.views import ASMLoginAPIView, RefreshTokenView, UserListView

urlpatterns = [
    path('login', LoginView.as_view()),
    path('addpincode', UploadAndProcessFileAPI.as_view()),

    path('refresh',RefreshTokenView.as_view()),

    path('logout',LogoutView.as_view()),

    path('users', UserListView.as_view(), name='user-list'),

    path('register', ASMRegisterAPI.as_view()),
]
