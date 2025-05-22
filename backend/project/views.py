from django.http import HttpResponse

def health(request):
    return HttpResponse('<h1>Backend is working.</h1>', status=200)