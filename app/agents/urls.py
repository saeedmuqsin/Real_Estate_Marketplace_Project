from django.urls import path
from . import views

app_name = "agents"

# create urls for app
urlpatterns = [ 
    path('dashboard/', view=views.agents_dashboard, name="agents_dashboard"),
    path('add_property/', view=views.add_property, name="add_property"),
    path("my_properties/", view=views.my_properties, name="my_properties"),
    path("inquiries/", view = views.inquiries, name="inquiries"),
    path("settings/", view = views.settings, name="settings"),
]