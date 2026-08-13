from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from app.view_access import owner_required
from django.contrib import messages
from properties.models import PropertyImage
from accounts.models import User, Profile

# Create your views here.
@owner_required
def agents_dashboard(request):
    id = request.GET.get('id')
    context =  { 
        "total_listings": request.user.profile.properties.all().count(),
        "Recent_Properties": request.user.profile.properties.all()
    }
    return render(request, "agents/dashboard.html", context)

@owner_required
def add_property(request):
    id = request.GET.get("id")
    return render(request, "agents/add_property.html")

@owner_required
def my_properties(request):
    id = request.GET.get("id")
    properties = request.user.profile.properties.all()
    context = {
        "properties": properties,
        'count_all': properties.count(),
        'count_active': properties.filter(status='active').count(),
        'count_pending': properties.filter(status='pending').count(),
        'count_sold': properties.filter(status='sold').count(),
    }
    return render(request, "agents/my_properties.html", context)

@owner_required
def settings(request):
    if request.method == "POST":
        username = request. POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        gender = request.POST.get("gender")
        profile_bio = request.POST.get('profile-bio')
        
        updateUser = User.objects.get(id = request.user.id)
        updateUser.name = username
        updateUser.email = email
        updateUser.gender = gender
        updateUser.phone_number = phone_number
        updateUser.save()

        Profile.objects.filter(userId=updateUser).update(bio = profile_bio)


        messages.success(request, "Profile updated")
        return redirect("agents:agents_dashboard")
    
 
    return render(request, "agents/settings.html")