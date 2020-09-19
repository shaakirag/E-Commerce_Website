from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('store:index'))
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

