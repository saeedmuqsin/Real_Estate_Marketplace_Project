from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from app.view_access import admin_required
from properties.models import Property
from accounts.models import Profile, User
from inquiries.models import Inquiry
import datetime
from django.db.models import Count
from django.db.models.functions import TruncMonth
import json

# Create your views here.


@admin_required
def admin_dashboard(request):
    current_year = datetime.datetime.now().year

    # Get monthly data for properties for current year
    properties_by_month = (
        Property.objects.filter(created_at__year=current_year)
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )


    # Get monthly data for inquiries for current year
    inquiries_by_month = (
        Inquiry.objects.filter(created_at__year=current_year)
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )

    # Create all 12 months for current year
    all_months = []
    for month_num in range(1, 13):
        all_months.append(datetime.date(current_year, month_num, 1))

    # Create month labels (January, February, etc.)
    month_labels = [month.strftime("%B") for month in all_months]

    # Map data to months
    properties_data = {}
    for item in properties_by_month:
        if item["month"]:
            properties_data[item["month"]] = item["count"]

    inquiries_data = {}
    for item in inquiries_by_month:
        if item["month"]:
            inquiries_data[item["month"]] = item["count"]

    # Create arrays matching all 12 months
    properties_counts = [properties_data.get(month, 0) for month in all_months]
    inquiries_counts = [inquiries_data.get(month, 0) for month in all_months]

    chart_data = {
        "labels": month_labels,
        "properties": properties_counts,
        "inquiries": inquiries_counts,
    }

    context = {
        "total_properties": Property.objects.all().count(),
        "total_agents": Profile.objects.all().count(),
        "total_customers": User.objects.filter(role="Customer").all().count(),
        "total_inquiries": Inquiry.objects.all().count(),
        "recent_properties": Property.objects.order_by("-created_at", "-price").all()[
            :10
        ],
        "chart_data": json.dumps(chart_data),
    }
    return render(request, "admin/dashboard.html", context)


@admin_required
def properties(request):
    context = {
        "properties": Property.objects.all(),
        "count_all": Property.objects.all().count(),
        "count_active": Property.objects.filter(status='active').count(),
        "count_pending": Property.objects.filter(status='pending').count(),
    }
    return render(request, "admin/properties.html", context)

@admin_required
def approve_properties(request, id):
    Property.objects.filter(id = id).update(status='active')
    messages.success('Property Approved Successfully')
    return redirect('admin:admin_dashboard')