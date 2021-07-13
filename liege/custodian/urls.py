from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from custodian import views as custodianviews

urlpatterns = [
    path("",custodianviews.index),
    path("uploaddocs",custodianviews.uploaddocs),
    path("viewpf/<int:id>/",custodianviews.pfsummary),
    path("transhistory/<int:id>/",custodianviews.transhistory),
    path("createclient",custodianviews.create_client),
    path("createholding/<int:id>/",custodianviews.create_holdings),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)