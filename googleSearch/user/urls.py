from django.urls import path
from . import views
from rest_framework import routers
from django.conf.urls import include
from knox import views as knox_views

ROUTER = routers.SimpleRouter(trailing_slash=True)
ROUTER.register(r'user', views.LoginApi, basename='user')

urlpatterns = [
    path('', include(ROUTER.urls)),
    path('api/auth/', include('djoser.urls')),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    path('search/', views.SearchedData.as_view(), name='search'),
    path('viewall/', views.ViewAll.as_view(), name='viewall'),
    path('savedata/', views.SaveData.as_view(), name='savedata')
]
