from django.http import HttpResponseForbidden

def owner_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == "Owner":
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden('Access Denied')
    return  wrapper

def customer_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == "Customer":
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Access Denied")
    return wrapper