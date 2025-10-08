from django.urls import path

from api.serializer import LoginSerializer
from api.views import UploadAndProcessFileAPI, ASMRegisterAPI, LoginView, LogoutView, UserProfileAPI
from asm.views import ASMLoginAPIView, RefreshTokenView, UserListView, ASMByZoneManagerAPIView

from asm.api_views import ASMTargetsListAPIView, ASMSetTargetAPIView, ASMDailyTargetAchievementListAPIView
from tasks.views import ASMTaskManageAPIView
from partner.api_views import SDCollectionListCreateAPIView, SDCollectionRetrieveUpdateAPIView

from zonemanager.api_views import ZMDailyTargetCreateAPIView, ZMDailyTargetListAPIView

urlpatterns = [
    path('login', LoginView.as_view()),
    path('addpincode', UploadAndProcessFileAPI.as_view()),

    path('refresh',RefreshTokenView.as_view()),

    path('logout',LogoutView.as_view()),

    path('users', UserListView.as_view(), name='user-list'),

    path('register', ASMRegisterAPI.as_view()),

    path('profile', UserProfileAPI.as_view()),

    path('asms',ASMByZoneManagerAPIView.as_view() ),

    path('zm-daily-target/',ZMDailyTargetCreateAPIView.as_view()),

    path('zm-daily-target-list',ZMDailyTargetListAPIView.as_view()),

    path('asm/targets/', ASMTargetsListAPIView.as_view(), name="asm-targets-list"),
    path('asm/set-target/', ASMSetTargetAPIView.as_view(), name="asm-set-target"),

    path("asm/targets-achievement/", ASMDailyTargetAchievementListAPIView.as_view(), name="asm-target-list"),


    # List all tasks or create a new task (POST)
    path("tasks/", ASMTaskManageAPIView.as_view(), name="asm-task-list-create"),

    # Retrieve, update (PUT/PATCH), or partially update a specific task
    path("tasks/<int:pk>/", ASMTaskManageAPIView.as_view(), name="asm-task-detail-update"),


    path("sdcollection/", SDCollectionListCreateAPIView.as_view(), name="sdcollection-list-create"),
    path("sdcollection/<int:pk>/", SDCollectionRetrieveUpdateAPIView.as_view(), name="sdcollection-detail-update"),

]
