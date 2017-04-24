from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from backend0bit import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'static-pages', views.StaticPageViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(
        r'^sp-reorder',
        views.reorder_staticpages,
        name='reorder-staticpages'
    ),
    url(r'^status', views.api_status, name='status')
]
