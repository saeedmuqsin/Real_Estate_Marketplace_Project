from django.urls import path
from . import views

app_name = "Admin"

urlpatterns = [
    path('dashboard/', view = views.admin_dashboard, name="admin_dashboard"),
    path('properties/', view=views.properties, name='properties')
]