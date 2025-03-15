from django.core.exceptions import ValidationError
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

# Global Response
# def custom_validation_exception_handler(exc, context):
#     print("Custom Validation Handler Called!")  # Debugging
#     response=exception_handler(exc, context)
#     if isinstance(exc, ValidationError):
#         return Response({
#             "status_code": status.HTTP_400_BAD_REQUEST,
#             "status": "error",
#             "message": "Validation error",
#             # "errors": response.data if response else exc.detail
#         }, status=status.HTTP_400_BAD_REQUEST)
#     return response

# def custom_404_exception_handler(exc, context):
#     response=exception_handler(exc, context)
#     if isinstance (exc, Http404):
#         return Response({
#             "status_code":status.HTTP_404_NOT_FOUND,
#             "status":"error",
#             "message":"the requested resource was not found"
#         }, status=status.HTTP_404_NOT_FOUND)
#     return response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # Menangani 404
    if isinstance(exc, Http404):
        print('4044444')
        return Response({
            "status_code": status.HTTP_404_NOT_FOUND,
            "status": "error",
            "message": "The requested resource was not found"
        }, status=status.HTTP_404_NOT_FOUND)

    # Menangani 400 ValidationError
    if isinstance(exc, ValidationError) or (response is not None and response.status_code == 400):
        print('400 Validation Error Detected')
        return Response({
            "status_code": status.HTTP_400_BAD_REQUEST,
            "status": "error",
            "message": "Validation error",
            "errors": exc.detail if isinstance(exc, ValidationError) else response.data
        }, status=status.HTTP_400_BAD_REQUEST)
        
    return response

# Manual Call Response
def success_response(serializer, message):
    return Response({
        "status_code":status.HTTP_200_OK,
        "status":"success",
        "message":message,
        "data":serializer
    }, status=status.HTTP_200_OK)

def created_response(serializer, message):
    return Response({
        "status_code":status.HTTP_201_CREATED,
        "status":"created",
        "message":message,
        "data":serializer
    }, status=status.HTTP_201_CREATED)

def delete_reponse():
    # return Response({
    #     "status_code":status.HTTP_204_NO_CONTENT,
    #     "status":"success",
    #     "message":"success delete data",
    #     "data":None
    # }, status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_204_NO_CONTENT)

def options_response():
    return Response({
            "status_code":status.HTTP_200_OK,
            "status":"success",
            "allow":["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
            "message":"These are the allowed methods for this endpoint."
        })

def error_400_response(serializer):
    return Response({
        "status_code": status.HTTP_400_BAD_REQUEST,
        "status": "error",
        "message": "invalid data",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

def error_400_integirty_response(message):
    return Response({
        "status_code": status.HTTP_400_BAD_REQUEST,
        "status": "error",
        "message": message,
        "errors":{"detail":[message]}
    }, status=status.HTTP_400_BAD_REQUEST)


# def internal_server_error_reponse(e):
#     return Response({
#         "status_code":status.HTTP_500_INTERNAL_SERVER_ERROR,
#         "status":"error",
#         "message":"Internal Server Error: ",
#         "error": str(e)
#     }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)