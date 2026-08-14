from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from app.view_access import owner_required
from django.contrib import messages
from properties.models import PropertyImage
from accounts.models import User, Profile
from properties.models import Property
from inquiries.models import Inquiry
from django.db.models import Count
from django.db.models.functions import TruncMonth
import datetime
import calendar
import json
from django.utils.safestring import mark_safe

# Create your views here.
@owner_required
def agents_dashboard(request):
    id = request.GET.get('id')
    # basic stats
    
    today = datetime.date.today()
    user_properties = request.user.profile.properties.filter(created_at__date=today)

    # aggregate properties per month for the current year
    current_year = datetime.date.today().year
    monthly_qs = Property.objects.filter(created_at__year=current_year).annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')

    # prepare a full 12-month series (Jan..Dec) with zeros for months without data
    month_counts = {m: 0 for m in range(1, 13)}
    for row in monthly_qs:
        m = row['month'].month
        month_counts[m] = row['count']

    labels = [calendar.month_name[m] for m in range(1, 13)]
    counts = [month_counts[m] for m in range(1, 13)]

    context =  {
        "total_listings": user_properties.count(),
        "Recent_Properties": user_properties,
        "total_active_properties" : request.user.profile.properties.filter(status='active').count(),
        "total_inquiries": Inquiry.objects.filter(profile=request.user.profile.id).count(),
        "monthly_labels_json": mark_safe(json.dumps(labels)),
        "monthly_counts_json": mark_safe(json.dumps(counts)),
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
def inquiries(request):
    context = { 
        'inquiries': Inquiry.objects.filter(profile = request.user.profile.id).all()
    }
    return render(request, 'agents/inquiries.html', context)

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