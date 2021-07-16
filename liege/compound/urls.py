from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from compound import views as compoundviews

urlpatterns = [
    path("<int:id>/",compoundviews.index),
    path("createaccount/<int:id>/",compoundviews.create_unittrust_holdings),
    path("fundtransfer/<int:id>/",compoundviews.transfer_funds),
    path("holding/<int:id>/",compoundviews.holdingview)

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)