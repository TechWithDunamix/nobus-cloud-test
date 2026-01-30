from ninja.errors import HttpError
from ._api  import router
from ._schemas import Register, LoginRequest, TokenResponse, RefreshTokenRequest
from django.http import HttpRequest
from api.models.user import User
from api.services import JWTService

@router.post("/login",
    summary="Login a user",
    description="Login a user with email and password.",
    response=TokenResponse
    )
def login(request, login_data: LoginRequest):
    try:
        user = User.objects.get(email=login_data.email)
    except User.DoesNotExist:
        raise HttpError(401, "Invalid email or password")
    
    if not user.check_password(login_data.password):
        raise HttpError(401, "Invalid email or password")
        
    if not user.is_active:
        raise HttpError(403, "User account is disabled")
        
    tokens = JWTService.create_token_pair(user.id, user.email)
    
    return tokens

@router.post("/refresh",
    summary="Refresh access token",
    description="Get a new access token using a refresh token.",
    response=TokenResponse
    )
def refresh_token(request, refresh_data: RefreshTokenRequest):
    try:
        new_access_token, payload = JWTService.refresh_access_token(refresh_data.refresh)
        
        return {
            "access": new_access_token,
            "refresh": refresh_data.refresh
        }
    except Exception as e:
        raise HttpError(401, str(e))

@router.post("/register",
    summary="Register a new user",
    description="Register a new user with email, full_name, and password.",
    )
def register(request : HttpRequest,register_request: Register):
    """Register a new user."""
    if User.objects.filter(email=register_request.email).exists():
        return {"message": "User with this email already exists."}

    User.objects.create_user(
        email=register_request.email,
        password=register_request.password,
        full_name=register_request.full_name
    )

    return {"message": "Register successful"}
