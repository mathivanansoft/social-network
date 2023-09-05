from rest_framework.exceptions import APIException

class FriendRequestTimeLimitException(APIException):
    status_code = 429
    default_detail = 'Not allowed to create more than 3 friend request per minute, try again later.'
    default_code = 'too_many_requests'

class FriendRequestException(APIException):
    status_code = 400
    default_code = "bad_request"