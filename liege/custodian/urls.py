from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from custodian import views as custodianviews

urlpatterns = [
    path("",custodianviews.index),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)