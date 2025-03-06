from rest_framework.response import Response
from rest_framework import status

def success_response(serializer, message):
    return Response({
        "status_code":status.HTTP_200_OK,
        "status":"success",
        "message":message,
        "data":serializer.data
    }, status=status.HTTP_200_OK)

def delete_reponse(message):
    return Response({
        "status_code":status.HTTP_204_NO_CONTENT,
        "status":"success",
        "message":"success delete data",
        "data":None
    }, status=status.HTTP_204_NO_CONTENT)

def options_response():
    return Response({
            "status_code":status.HTTP_200_OK,
            "status":"success",
            "allow":["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
            "message":"These are the allowed methods for this endpoint."
        })