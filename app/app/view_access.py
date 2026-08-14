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

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_active == True and request.user.is_staff == True and request.user.is_superuser == True:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Access Denied")
    return wrapper
