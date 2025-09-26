# asm_management/middleware/auth_middleware.py
import jwt
from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import User, Group

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return JsonResponse({"error": "Authorization header missing"}, status=401)

        try:
            prefix, token = auth_header.split(" ")
            if prefix.lower() != "bearer":
                return JsonResponse({"error": "Invalid token prefix"}, status=401)

            # Decode token
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
            request.user_id = payload.get("user_id")  # attach to request for later use
            try:
                temp_user = User.objects.get(id=request.user_id)
                if temp_user.groups.filter(name='admin').exists():
                    request.user = temp_user
                    request.usertype = 'Admin'
                elif temp_user.groups.filter(name='ASM').exists():
                    request.user = temp_user
                    request.usertype = 'ASM'
                elif temp_user.groups.filter(name='Zonal Manager').exists():
                    request.user = temp_user
                    request.usertype = 'Zonal Manager'
                else:
                    return JsonResponse({"error": "Unable to find user role"},status=401)
            except Group.DoesNotExist:
                return JsonResponse({"error": "Group not found"},status=401)
            except User.DoesNotExist:
                return JsonResponse({"error": "User not found"}, status=401)

        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)
