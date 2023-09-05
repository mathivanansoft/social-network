from rest_framework.response import Response
from rest_framework import status

def generate_response(data=None, message=None, status_code=status.HTTP_200_OK):
    response_data = {
        "status": "success",
        "message": message or "Data retrieved",
        "data": data,
    }
    return Response(response_data, status=status_code)


def generate_error_response(data=None, message=None, status_code=status.HTTP_400_BAD_REQUEST):
    response_data = {
        "status": "error",
        "message": message or "No data found",
        "data": None,
    }
    return Response(response_data, status=status_code)
