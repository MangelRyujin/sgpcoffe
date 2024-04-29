from django.http import HttpResponseRedirect
from django.urls import reverse

class RedirectAfterLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path == '/admin/login/' and request.method == 'POST':
            return HttpResponseRedirect('/')
        return response