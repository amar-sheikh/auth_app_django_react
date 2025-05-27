from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
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
            'last_name': user.last_name
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

require_http_methods(['POST'])
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

require_http_methods(['POST'])
def send_reset_password_email(request):
    try:
        data = json.loads(request.body)
        user = User.objects.get(username=data['username'])

        origin = request.headers['Origin']
        url = f"{origin}{data['redirect']}"

        html = render_to_string('emails/reset_password.html', {
            'name': user.username,
            'url': url,
            'uid': urlsafe_base64_encode(force_bytes(user.id)),
            'token': default_token_generator.make_token(user)
        })

        msg = EmailMultiAlternatives(
            'Reset password',
            '',
            settings.EMAIL_HOST_USER,
            [user.email]
        )

        msg.attach_alternative(html, "text/html")
        msg.send()

        return JsonResponse({ 'message': 'Mail send successfully successfully' }, status=200)
    except Exception as e:
        return JsonResponse({ 'error': str(e) }, status=401)

require_http_methods(['POST'])
def reset_password(request):
    try:
        data = json.loads(request.body)
        id = urlsafe_base64_decode(data['uid']).decode()
        user = User.objects.get(pk=id)

        if default_token_generator.check_token(user, data['token']):
            form = SetPasswordForm(user=user,data={ 'new_password1': data['new_password1'], 'new_password2': data['new_password2'] })

            if form.is_valid():
                form.save()
                return JsonResponse({'message': 'Password reset successfully'}, status=200)
            else:
                return JsonResponse({'error': form.errors}, status=400)
        else:
            return JsonResponse({'error': 'Invalid or expired token'}, status=400)
    except Exception as e:
        return JsonResponse({ 'error': str(e) }, status=401)
