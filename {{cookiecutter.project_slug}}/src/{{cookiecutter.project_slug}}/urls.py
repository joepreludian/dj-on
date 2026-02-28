from ninja import NinjaAPI
from django.contrib import admin
from django.urls import path

api = NinjaAPI()


@api.get("/health")
def health(request):
    return {"status": "ok"}


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
