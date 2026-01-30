from ninja import NinjaAPI
from api.routers.auth import router as auth_router
from api.routers.loans import router as loans_router
from api.routers.admin import router as admin_router

api = NinjaAPI()
api.add_router("/auth", auth_router, tags=["Auth"])
api.add_router("/loans", loans_router, tags=["Loans"])
api.add_router("/admin", admin_router, tags=["Admin"])
@api.get("/hello")
def hello(request):
    return {"hello": "world"}
