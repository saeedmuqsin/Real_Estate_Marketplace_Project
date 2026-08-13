import uuid
from django.db import models
import base64
from builtins import property as builtin_property

# Create your models here.
class Property(models.Model):
    PROPERTY_TYPES = [
        ('House', 'House'),
        ('Apartment', 'Apartment'),
        ('Commerical', 'Commerical'),
        ('Land', 'Land'),
        ('Villa', 'Villa')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    listing_type = models.CharField(max_length=10, choices=[('Sale', 'Sale'), ('Rent', 'Rent')])
    price = models.PositiveIntegerField(default=None)
    location = models.CharField(max_length=100)
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    area_size = models.PositiveIntegerField()
    furnishing = models.CharField(max_length=25, default=None)
    google_map_link = models.CharField(max_length=250, default=None)
    status = models.CharField(max_length=10, default="pending")
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name='properties', default=None)

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.BinaryField()
    image_name = models.CharField(max_length=255, default=None)
    image_type = models.CharField(max_length=255, default=None)

    @builtin_property
    def image_base64(self):
        return base64.b64encode(self.image).decode("utf-8")