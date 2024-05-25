from django.contrib import admin
from django.urls import path, include
from users.views import UserSignupView, UserSearchView, SendFriendRequestView, RespondFriendRequestView, FriendsListView, PendingFriendRequestsView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/signup/', UserSignupView.as_view(), name='signup'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/search/', UserSearchView.as_view(), name='search'),
    path('api/friend-request/send/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('api/friend-request/respond/<int:request_id>/', RespondFriendRequestView.as_view(), name='respond-friend-request'),
    path('api/friends/', FriendsListView.as_view(), name='friends-list'),
    path('api/friend-requests/pending/', PendingFriendRequestsView.as_view(), name='pending-friend-requests'),
]
