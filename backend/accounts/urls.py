from django.urls import path
from . import views

urlpatterns = [
    path('csrf', views.csrf_view, name='csrf'),
    path('whoami', views.whoami_view, name='whoami'),
    path('register', views.register_view, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('update', views.update_user_view, name='update'),
    path('update-password', views.update_password_view, name='update-password'),
    path('send-password-reset-email', views.send_reset_password_email, name='send-password-reset-email'),
    path('reset-password', views.reset_password, name='reset-password'),
]
