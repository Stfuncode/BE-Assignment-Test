from django.urls import path

# views
from .views import InventoryApiListView

urlpatterns = [
    path('', InventoryApiListView.as_view(), name='api_inventory_list'),
]