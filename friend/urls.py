from django.urls import path

from .views import FriendRequestAPIView, ListFriendAPIView, ListFriendRequestPendingAPIView

urlpatterns = [
   path("request-accepted/", ListFriendAPIView.as_view()),
   path("request-pending/", ListFriendRequestPendingAPIView.as_view()),
   path("<int:friend_id>/friend-request/", FriendRequestAPIView.as_view()),

]
