from django.shortcuts import render
from django.core.validators import validate_email
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions, status, generics

from .models import FriendRequest, Friendship
from .serializers import FriendshipSerializer
from .exceptions import FriendRequestException, FriendRequestTimeLimitException 
from account.models import CustomUser
from account.serializers import CustomUserReadSerializer
from utils.response import generate_response
from utils import response_message


class FriendRequestAPIView(APIView):
    def post(self, request, friend_id):
        user = request.user
        one_minute_ago = timezone.now() - timedelta(minutes=60)
        count = FriendRequest.objects.filter(from_user=user, created_at__gte=one_minute_ago).count()
        if count >= settings.FRIEND_REQUEST_LIMIT:
            raise FriendRequestTimeLimitException()

        friend = CustomUser.objects.filter(id=friend_id).first()
        if friend is None:
            raise exceptions.ParseError(response_message.FRIEND_NOT_FOUND)

        if Friendship.objects.filter(Q(from_user=user, to_user=friend)|Q(from_user=friend, to_user=user)):
            return generate_response(data=None, message=response_message.ALREADY_FRIEND.format(username=friend.username))

        friend_request = FriendRequest.objects.filter(Q(from_user=user, to_user=friend)|Q(from_user=friend, to_user=user)).first()
        if friend_request is not None:
            # readability
            if friend_request.request_status == FriendRequest.RequestStatus.PENDING:
                if friend_request.from_user == user:
                    return generate_response(data=None, message=response_message.FR_ALREADY_SENT.format(username=friend.username))
                else:
                    friend_request.request_status = FriendRequest.RequestStatus.ACCEPT
                    friend_request.save()
                    Friendship.objects.create(from_user=friend, to_user=user)
                    return generate_response(data=None, message=response_message.FR_ACCEPTED.format(username=friend.username))
            else:
                friend_request.from_user = user
                friend_request.to_user = friend
                friend_request.request_status = FriendRequest.RequestStatus.PENDING
                friend_request.save()
                return generate_response(data=None, message=response_message.FR_SUCCESS.format(username=friend.username))
        else:
            friend_request = FriendRequest.objects.create(from_user=user, to_user=friend)
            return generate_response(data=None, message=response_message.FR_SUCCESS.format(username=friend.username))

    def put(self, request, friend_id):
        user = request.user
        friend = CustomUser.objects.filter(id=friend_id).first()
        friend_request = FriendRequest.objects.filter(from_user=friend, to_user=user).first()
        if friend is not None and friend_request is not None and friend_request.request_status == friend_request.RequestStatus.PENDING:
            friend_request.request_status = FriendRequest.RequestStatus.ACCEPT
            friend_request.save()
            Friendship.objects.create(from_user=friend, to_user=user)
            return generate_response(data="", message=response_message.FR_ACCEPTED.format(username=friend.username))
        else:
            raise FriendRequestException(response_message.FR_NOT_SEND.format(username=friend.username))
        
    def delete(self, request, friend_id):
        user = request.user
        friend = CustomUser.objects.filter(id=friend_id).first()
        friend_request = FriendRequest.objects.filter(from_user=friend, to_user=user).first()
        if friend is not None and friend_request is not None:
            if friend_request.request_status == friend_request.RequestStatus.PENDING:
                friend_request.request_status = FriendRequest.RequestStatus.REJECT
                friend_request.save()
            else:
                raise FriendRequestException(response_message.FR_NOT_SEND.format(username="user-id:"+ str(friend_id)))
        else:
            raise FriendRequestException(response_message.FR_NOT_SEND.format(username="user-id:"+ str(friend_id)))
        return generate_response(data=None, message=response_message.FR_REJECTED.format(username=friend.username))


class ListFriendAPIView(generics.ListAPIView):
    serializer_class = CustomUserReadSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = CustomUser.objects.filter(Q(friendship_creator__to_user=user)|Q(friendship_receiver__from_user=user)).order_by('-id').distinct()
        return queryset


class ListFriendRequestPendingAPIView(generics.ListAPIView):
    serializer_class = CustomUserReadSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = CustomUser.objects.filter(
            friend_requests_sent__to_user=user,
            friend_requests_sent__request_status=FriendRequest.RequestStatus.PENDING
        ).order_by('-id').distinct()
        return queryset