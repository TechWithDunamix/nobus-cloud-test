from ninja.security import HttpBearer
from .jwt_service import JWTService
from api.models.user import User

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = JWTService.decode_token(token)
            if payload:
                user = User.get_user_or_none(payload["user_id"])
                return user
        except Exception as e:
           return None
