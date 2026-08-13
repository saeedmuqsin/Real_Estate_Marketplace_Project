from django.shortcuts import redirect, get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from properties.models import Property
from .models import Inquiry
from .services import InquiryService
from app.view_access import customer_required
from django.urls import reverse

# Create your views here.


@customer_required
def start_inquiry(request, id):
    # querying for property object using the id
    property = get_object_or_404(Property, id=id)

    # creating a new inquiry
    inquiry = InquiryService.create_or_get_inquiry(
        customer=request.user,
        property=property,
    )

    # creates an intial messages that will show interestings
    # InquiryMessage.objects.create(
    #     inquiry = inquiry,
    #     sender = request.user,
    #     messages = (f'Hello {property.owner.name}, I am interested in {property.title}')
    # ).save()

    return redirect("customers:customer_inquiries")


@customer_required
def conversation(request, id):
    inquiry = get_object_or_404(Inquiry, id=id)

    # checking for security
    if request.user not in [inquiry.customer, inquiry.profile.userId]:
        messages.error(request, "Your are not include here")

        return render(request, "customer:dashboard")

    chat_messages = inquiry.messages.all()
    chat_messages.filter(is_read=False, inquiry=inquiry).exclude(sender=request.user).update(is_read=True)

    return JsonResponse(
        {
            "inquiry": {
                "id": inquiry.id,
                "agent_name": inquiry.profile.userId.name,
                "agent_email": inquiry.profile.userId.email,
                "agent_phone": inquiry.profile.userId.phone_number,
                "date": inquiry.created_at,
                "status": inquiry.status,
                "property": {
                    "id": inquiry.property.id,
                    "title": inquiry.property.title,
                    "location": inquiry.property.location,
                    "price": inquiry.property.price,
                    "image_type": (
                        inquiry.property.images.first().image_type
                        if inquiry.property.images.exists()
                        else None
                    ),
                    "image_base64": (
                        inquiry.property.images.first().image_base64
                        if inquiry.property.images.exists()
                        else None
                    ),
                },
            },
            "current_user": request.user.id,
            "messages": [
                {
                    "id": message.id,
                    "sender": {
                        "id": message.sender.id,
                        "name": message.sender.name,
                        "is_me": message.sender == request.user,
                    },
                    "message": message.message,
                    "date": message.created_at.isoformat(),
                }
                for message in chat_messages
            ],
        }
    )
