"""cloudyweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.authtoken import views as authtoken_views
from rest_framework import routers
from accounts import views as accounts_views
from cloudygames import views as cloudygames_views

router = routers.DefaultRouter()
router.register(r'users', accounts_views.UserViewSet)
router.register(r'games', cloudygames_views.GameViewSet)
router.register(r'game-ownership', cloudygames_views.GameOwnershipViewSet)
router.register(r'game-session', cloudygames_views.GameSessionViewSet)
router.register(r'save-data', cloudygames_views.PlayerSaveDataViewSet)

admin.site.site_header = 'CloudyPanel'

urlpatterns = router.urls + [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', 
        include('rest_framework.urls', 
        namespace='rest_framework')),
    url(r'^api-token-auth/tokens/',
        accounts_views.obtain_auth_token,
        name='token-auth'),
    url(r'^api-token-auth/', include('rest_framework_registration.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
