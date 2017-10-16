from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from backend0bit.views import (StaticPageViewSet, reorder_staticpages,
                               api_status)
from posts.views import PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, base_name='post')
router.register(r'static-pages', StaticPageViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^sp-reorder', reorder_staticpages, name='reorder-staticpages'),
    url(r'^status', api_status, name='status')
]
