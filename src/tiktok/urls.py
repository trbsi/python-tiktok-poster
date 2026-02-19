from django.urls import path

from . import views

urlpatterns = [
    path('redirect-to-tiktok', views.auth_redirect_to_tiktok, name='tiktok.auth_redirect_to_tiktok'),
    path('redirect-from-tiktok', views.auth_redirect_from_tiktok, name='tiktok.auth_redirect_from_tiktok'),
]
