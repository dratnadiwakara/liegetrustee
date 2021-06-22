from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .import views

urlpatterns = [
    path("",views.index),
    path("create_borrower",views.create_borrower_view),
    path("create_securitization",views.create_securitization_view),
    path("update_securitization_trustee/<int:id>/",views.update_securitization_trustee_view),
    path("update_securitization_arranger/<int:id>/",views.update_securitization_arranger_view),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)