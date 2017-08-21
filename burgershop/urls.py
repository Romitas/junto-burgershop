from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from rest_framework import routers
from rest_framework.authtoken import views as authtoken_views
from rest_framework.schemas import get_schema_view

from . import views
from .models import Order

app_name = 'burgershop'

#schema_view = get_schema_view(title='Users API', renderer_classes = [OpenAPIRenderer, SwaggerUIRenderer])

router = routers.DefaultRouter()
router.register(r'menu', views.CategoryViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'orderrows', views.OrderRowViewSet)
router.register(r'items', views.ItemViewSet)

urlpatterns = [
        url(r'^', include(router.urls), name='index'),
        url(r'auth-api-token/', authtoken_views.obtain_auth_token),
        url(r'login/?$', views.login_form, name='login_form'),
        url(r'login/check/?$', views.login_validate, name='login_validate'),
        url(r'logout/?$', views.login_logout, name='login_logout'),
        ]
