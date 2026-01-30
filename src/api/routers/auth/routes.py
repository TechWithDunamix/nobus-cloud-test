from ._api  import router
from ._schemas import Register
from django.http import HttpRequest
from api.models.user import User
@router.post("/login",
    summary="Login a user",
    description="Login a user with email and password.",
    )
def login(request):
    return {"message": "Login successful"}

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
