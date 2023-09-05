from django.db import models

from account.models import CustomUser
# Create your models here.

class Friendship(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="friendship_creator")
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="friendship_receiver")
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints= [
            models.UniqueConstraint(name="unique_friend", fields=["from_user", "to_user"])
        ]


class FriendRequest(models.Model):
    class RequestStatus(models.IntegerChoices):
        PENDING = 1
        ACCEPT = 2
        REJECT = 3

    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="friend_requests_sent")
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="friend_requests_received")
    request_status = models.IntegerField(choices=RequestStatus.choices, default=RequestStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints= [
            models.UniqueConstraint(name="unique_friend_request", fields=["from_user", "to_user"])
        ]