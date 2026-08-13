from django.urls import re_path

from .consumers import InquiryConsumer


websocket_urlpatterns = [
    re_path(
        r"ws/inquiries/(?P<inquiry_id>[0-9a-f-]+)/$",
        InquiryConsumer.as_asgi(),
    ),
]