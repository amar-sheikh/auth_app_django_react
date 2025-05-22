from django.urls import path
from . import views

urlpatterns = [
    path('csrf', views.csrf_view),
    path('whoami', views.whoami_view),
    path('register', views.register_view),
    path('login', views.login_view),
    path('logout', views.logout_view),
    path('update', views.update_user_view),
    path('update-password', views.update_password_view)
]
