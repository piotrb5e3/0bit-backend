from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from backend0bit import views

# Create a router and register our viewsets with it.
router = DefaultRouter(trailing_slash=False)
router.register(r'posts', views.PostViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]