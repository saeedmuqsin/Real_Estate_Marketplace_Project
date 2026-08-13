from django.urls import path
from . import views

app_name = "customers"

urlpatterns = [
    path('', view=views.dashboard, name="dashboard"),
    path('properties/', view=views.properties, name="properties"),
    path('inquiries', views.customer_inquiries, name="customer_inquiries"),
    path('settings/', views.settings, name="settings"),
    path('delete_account/', views.delete_account, name="delete_account")
]