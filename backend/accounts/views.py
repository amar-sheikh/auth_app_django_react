from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.models import User
import json
from .forms import CustomUserCreationForm, CustomUserChangeForm

@ensure_csrf_cookie
def csrf_view(request):
    return JsonResponse({'message': 'CSRF token set successfully'}, status=200)

def whoami_view(request):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)

        return JsonResponse({ 'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_joined': user.date_joined
        }}, status=200)
    return JsonResponse({'message': 'User is not authenticated.'}, status=401)

require_http_methods(['POST'])
def register_view(request):
    data = json.loads(request.body)

    form = CustomUserCreationForm(data)

    if form.is_valid():
        form.save()
        return JsonResponse({'message': 'User registered successfully'}, status=201)
    else:
        return JsonResponse({'errors': form.errors}, status=400)

require_http_methods(['POST'])
def login_view(request):
    data = json.loads(request.body)
    user = authenticate(request, username=data['username'], password=data['password'])
    
    if user:
        login(request, user)
        return JsonResponse({ 'message': 'User logged in successfully' }, status=200)
    else:
        return JsonResponse({ 'message': 'Invalid credential: Either User name or password is incorrect' }, status=401)

require_http_methods(['POST'])
def logout_view(request):
    logout(request)
    return JsonResponse({ 'message': 'Logged out successfully' }, status=200)

require_http_methods(['POST'])
def update_user_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    data = json.loads(request.body)
    form = CustomUserChangeForm(data, instance=request.user)

    if form.is_valid():
        form.save()
        return JsonResponse({ 'message': 'User updated successfully' }, status=200)
    else:
        return JsonResponse({'errors': form.errors}, status=400)

def update_password_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    data=json.loads(request.body)
    form = PasswordChangeForm(user=request.user, data=data)

    if form.is_valid():
        form.save()
        update_session_auth_hash(request, form.user)
        return JsonResponse({ 'message': 'Password changed successfully' }, status=200)
    else:
        return JsonResponse({'errors': form.errors}, status=400)