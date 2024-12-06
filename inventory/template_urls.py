from django.urls import path

# views
from .views import InventoryListView, InventoryDetailView

urlpatterns = [
    path('', InventoryListView.as_view(), name='inventory_list'),
    path('<int:id>/', InventoryDetailView.as_view(), name='inventory_detail'),
]