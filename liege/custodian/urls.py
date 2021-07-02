from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from custodian import views as custodianviews

urlpatterns = [
    path("",custodianviews.index),
    path("uploaddocs",custodianviews.uploaddocs),
    path("viewpf",custodianviews.pfsummary),
    path("transhistory",custodianviews.transhistory),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)