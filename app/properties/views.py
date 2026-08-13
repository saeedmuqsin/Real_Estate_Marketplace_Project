from operator import le

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from app.view_access import customer_required, owner_required
from django.contrib import messages
from properties.models import Property, PropertyImage

# Create your views here.

@customer_required
def property_details(request):
    property_id = request.GET.get('property_id')

    property = Property.objects.filter(id=property_id).first()
    context = { 
        "property": property
    }
    return render(request, "properties/property_details.html", context)

@owner_required
def add_property(request):
    if request.method == "POST":
        # Handle form submission and save the property
        # You can access form data using request.POST and request.FILES
        # For example:
        title = request.POST.get('property_title')
        property_type = request.POST.get('property_type')
        description = request.POST.get('description')
        listing_type = request.POST.get('listing_type')
        price = request.POST.get('price')
        location = request.POST.get('location')
        bedrooms = request.POST.get('bedrooms')
        bathrooms = request.POST.get('bathrooms')
        area_size = request.POST.get('area_size')
        furnishing = request.POST.get('furnishing')
        google_map_link = request.POST.get('google_map_link')

        

        # Create a new Property instance and save it to the database
        new_property = Property(
            title=title,
            description=description,
            property_type=property_type,
            listing_type=listing_type,
            price=price,
            location=location,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            area_size=area_size,
            furnishing=furnishing,
            google_map_link=google_map_link,
            owner=request.user.profile  # Assuming the logged-in user is the owner
        )

        new_property.save()

        # Saving images of the properties in the database
        for file in request.FILES.getlist('property_images'):
            PropertyImage.objects.create(
                property=new_property,
                image = file.read(),
                image_name = file.name,
                image_type = file.content_type
            ).save()
        
        messages.success(request, "Property added successfully.")
        return redirect(reverse("agents:agents_dashboard")+f"?id={request.user.id}")

        
@owner_required
def delete_property(request, id):
    deleting_property = request.user.profile.properties.filter(id=id).first()
    deleting_property.delete()
    messages.success(request, "Property deleted successfully.")
    return redirect(reverse("agents:agents_dashboard")+f"?id={request.user.id}")