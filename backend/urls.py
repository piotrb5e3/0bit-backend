from django.conf.urls import include, url
from rest_framework_jwt.views import refresh_jwt_token

urlpatterns = [
    url(r'^auth/refresh', refresh_jwt_token),
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^', include('backend0bit.urls')),
]
