from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .models import FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer
from django.db.models import Q
from rest_framework.throttling import UserRateThrottle

User = get_user_model()

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        return User.objects.filter(
            Q(email__icontains=query) |
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        ).distinct()

class FriendRequestRateThrottle(UserRateThrottle):
    rate = '3/min'

class SendFriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [FriendRequestRateThrottle]

    def post(self, request):
        to_user_id = request.data.get('to_user_id')
        to_user = User.objects.get(id=to_user_id)
        from_user = request.user
        fr = FriendRequest.objects.filter(from_user=from_user, to_user=to_user)
        if fr.exists():
            return Response({"message": f"Friend request already sent! request_id {fr[0].id}"}, status=status.HTTP_400_BAD_REQUEST)

        fr = FriendRequest.objects.create(from_user=from_user, to_user=to_user)
        return Response({"message": f"Friend request sent. request_id {fr.id}"}, status=status.HTTP_201_CREATED)

class RespondFriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, request_id):
        friend_request = FriendRequest.objects.get(id=request_id)
        action = request.data.get('action')

        if friend_request.to_user != request.user:
            return Response({"message": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        if action == 'accept':
            friend_request.is_accepted = True
            friend_request.save()
        elif action == 'reject':
            friend_request.delete()

        return Response({"message": "Action performed"}, status=status.HTTP_200_OK)

class FriendsListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friends = FriendRequest.objects.filter(
            Q(from_user=user, is_accepted=True) | Q(to_user=user, is_accepted=True)
        )
        friend_ids = [f.to_user.id if f.from_user == user else f.from_user.id for f in friends]
        return User.objects.filter(id__in=friend_ids)

class PendingFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, is_accepted=False)
