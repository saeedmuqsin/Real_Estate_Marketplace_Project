from django.urls import path
from . import views

app_name = "properties"

urlpatterns = [
    path('details/', view=views.property_details, name="property_details"),
    path('add_property/', view=views.add_property, name="add_property"),
    path('delete_property/<uuid:id>/delete', view=views.delete_property, name='delete_property')
]