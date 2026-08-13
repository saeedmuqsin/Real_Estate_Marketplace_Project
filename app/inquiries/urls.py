from django.urls import path
from . import views

app_name = "inquiries"

urlpatterns = [
    path('start/<uuid:id>', view = views.start_inquiry, name='start_inquiry'),
    path('conversation/<uuid:id>', view=views.conversation, name='conversation')
]