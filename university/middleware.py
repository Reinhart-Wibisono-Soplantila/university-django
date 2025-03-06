from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
import traceback

class CustomExceptionMiddleware(MiddlewareMixin):
    def exception_reponse_global(self, request, exception):
        print(traceback.format_exc())
        return JsonResponse({
            "status_code":'HTTP_500_INTERNAL SERVER ERROR',
            "message": "Internal Server Error", 
            "error": str(exception)
        })