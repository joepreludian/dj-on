from ninja import NinjaAPI
from django.contrib import admin
from django.urls import path
from base.api import router as base_router

api = NinjaAPI()

api.add_router("/", base_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
