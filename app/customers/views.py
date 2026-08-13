from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from app.view_access import customer_required
from properties.models import Property
from inquiries.models import  Inquiry
from accounts.models import User, Profile
# Create your views here.

@customer_required
def dashboard(request):
    best_properties = Property.objects.filter(
    status="active"
).order_by("-created_at")[:3]
    context = { 
        "properties": best_properties
    }
    return render(request, 'customers/home.html', context)

@customer_required
def properties(request):
    context = {}
    if request.method == "POST":
        location = request.POST.get('location',"")
        property_type = request.POST.get('property_type',"")
        price_range = request.POST.get('price_range',"")
        bedrooms = request.POST.get('bedrooms',"")
        bathrooms = request.POST.get('bathrooms',"")

        query = (f"location={location}&property_type={property_type}&price_range={price_range}&bedrooms={bedrooms}&bathrooms={bathrooms}")
        return redirect(reverse("properties")+query)
    
    location = request.GET.get('location', "")
    property_type = request.GET.get("property_type", "")
    price_range = request.GET.get("price_range", "")
    bedrooms = request.GET.get('bedrooms', '')
    bathrooms = request.GET.get("bathrooms", '')

    # filtering querySet from the property table
    properties = Property.objects.all()

    if location:
        properties=properties.filter(location=location)

    if property_type:
        properties = properties.filter(property_type = property_type)

    if  price_range:
        min_price, max_price = map(int, price_range.split('-'))
        properties = properties.filter(price__gte=min_price, price__lte=max_price)

    context['properties'] = properties
    context['location'] = location

    return render(request, 'customers/properties.html', context)

@customer_required
def customer_inquiries(request):
    # getting all inquiries made
    inquires = Inquiry.objects.filter(
        customer = request.user,
    ).select_related('property', 'profile')
    

    contexts = {
        "inquiries": inquires
    }

    return render(request, "inquiries/Customer_InquiryChat.html", contexts)


@customer_required
def settings(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone-number')
        gender = request.POST.get('gender')

        user = User.objects.get(id=request.user.id)
        user.name = username
        user.gender = gender
        user.phone_number = phone_number
        user.email = email
        user.save()

        return redirect(reverse("customers:dashboard"))

    return render(request, "customers/settings.html")

@customer_required
def delete_account(request):
    deleteUser = User.objects.get(id = request.user.id)
    deleteUser.delete()
    messages.success(request, "Account has been deleted successfully")
    return redirect("accounts:login")
