from django.db import transaction
from .models import Inquiry, InquiryMessage




class InquiryService:

    @staticmethod
    @transaction.atomic

    def create_or_get_inquiry(*, property, customer):

        if property.owner.userId == customer:
            raise Exception(
                "You cannot inquire about your own property"
            )

        inquiry, created = Inquiry.objects.get_or_create(
            property = property,
            customer = customer,
            profile = property.owner
        )

       
        return inquiry