from rest_framework.response import Response
from rest_framework import status

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

def delete_reponse(message):
    return Response({
        "status_code":status.HTTP_204_NO_CONTENT,
        "status":"success",
        "message":"success delete data",
        "data":None
    }, status=status.HTTP_204_NO_CONTENT)

# def created_response(data=None, message="Created"):
#     """ Response sukses dengan status 201 """
#     return Response({"message": message, "data": data}, status=status.HTTP_201_CREATED)

# def bad_request_response(message="Bad Request"):
#     """ Response error dengan status 400 """
#     return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

# def unauthorized_response(message="Unauthorized"):
#     """ Response error dengan status 401 """
#     return Response({"message": message}, status=status.HTTP_401_UNAUTHORIZED)

# def not_found_response(message="Not Found"):
#     """ Response error dengan status 404 """
#     return Response({"message": message}, status=status.HTTP_404_NOT_FOUND)

def options_response():
    return Response({
            "status_code":status.HTTP_200_OK,
            "status":"success",
            "allow":["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
            "message":"These are the allowed methods for this endpoint."
        })

def internal_server_error_reponse(e):
    return Response({
        "status_code":status.HTTP_500_INTERNAL_SERVER_ERROR,
        "status":"error",
        "message":"Internal Server Error: " + str(e)
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)