from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
import traceback
from rest_framework import status

class CustomExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        print(traceback.format_exc())
        return JsonResponse({
            "status_code":'HTTP_500_INTERNAL SERVER ERROR',
            "status":"error",
            "message": "Internal Server Error", 
            "error": str(exception)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)