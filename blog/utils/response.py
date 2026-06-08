from rest_framework.response import Response
from rest_framework import status


def success_response(data=None, message="Success", status_code=200):
    return Response(
        {
            "success": True,
            "message": message,
            "data": data
        },
        status=status_code
    )


def error_response(message="Error", status_code=400, data=None):
    return Response(
        {
            "success": False,
            "message": message,
            "data": data
        },
        status=status_code
    )