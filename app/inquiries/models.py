from django.db import models
from accounts.models import User, Profile
from properties.models import Property
import uuid

# Create your models here.
class Inquiry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        CLOSED = "CLOSED", "Closed"

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="inquiries")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer_inquires")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="owner_inquires")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [

            models.Index(
                fields=[
                    "customer",
                    "status"
                ]
            ),


            models.Index(
                fields=[
                    "profile",
                    "status"
                ]
            ),


            models.Index(
                fields=[
                    "property"
                ]
            ),

        ]

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "property",
                    "customer",
                ],
                name="unique_property_customer_inquiry"
            )

        ]


    def __str__(self):
        return (f"{self.customer.email} - " f"{self.property.title}")


    def close(self):
        self.status = self.Status.CLOSED
        self.save(update_fields=["status"])

    def reopen(self):
        self.status = self.Status.OPEN
        self.save(update_fields=['status'])

    def last_message(self):
        return (
            self.messages
            .order_by("-created_at")
            .first()
        )


    def unread_messages(self, user):
        return (
            self.messages
            .filter(
                is_read=False
            )
            .exclude(
                sender=user
            )
        )


class InquiryMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    inquiry = models.ForeignKey(Inquiry, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [

            models.Index(
                fields=[
                    "inquiry",
                    "created_at"
                ]
            ),


            models.Index(
                fields=[
                    "sender",
                    "is_read"
                ]
            )

        ]


    def __str__(self):

        return (
            f"{self.sender.email}: "
            f"{self.message[:30]}"
        )

    def mark_as_read(self):
        self.is_read=True
        self.save(update_fields=["is_read"])
