from ninja import NinjaAPI
from api.routers.auth import router as auth_router
api = NinjaAPI()
api.add_router("/auth", auth_router,tags=["Auth"])
@api.get("/hello")
def hello(request):
    return {"hello": "world"}
