from ninja.security import HttpBearer
from .jwt_service import JWTService
from api.models.user import User

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = JWTService.validate_access_token(token)
            if payload:
                user = User.objects.filter(id=payload["user_id"]).first()
                if user and user.is_active:
                    return user
            return None
        except Exception:
           return None

class AdminAuth(AuthBearer):
    def authenticate(self, request, token):
        user = super().authenticate(request, token)
        if user and user.is_staff:
            return user
        return None