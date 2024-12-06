from django.views.generic import ListView, DetailView
from django.http import Http404

# DRF
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# models
from .models import Inventory

# serializers
from .serializers import InventorySerializer

# exceptions
from .exceptions import NotFound

# services
from .services import InventoryService


class InventoryListView(ListView):
    model = Inventory
    context_object_name = 'inventories'
    template_name = 'inventory/inventory_list.html'

    def get_queryset(self):
        inventory_service = InventoryService()
        return inventory_service.get_inventories()
    


class InventoryDetailView(DetailView):
    model = Inventory
    context_object_name = 'inventory'
    template_name = 'inventory/inventory_detail.html'

    def get_object(self):
        id = self.kwargs['id']
        try:
            inventory_service = InventoryService()
            return inventory_service.get_inventory(id)
        except NotFound:
            raise Http404("Inventory item not found")
        

# API
class InventoryApiListView(APIView):
    def get(self, request):
        name = request.GET.get('name', None)
        supplier = request.GET.get('supplier', '')
        stock = request.GET.get('stock')
        availability = request.GET.get('availability')

        try:
            inventory_service = InventoryService()
            inventories = inventory_service.get_inventories(
                name=name,
                supplier=supplier,
                stock=stock,
                availability=availability
            )

            serializer = InventorySerializer(inventories, many=True)
            return Response({
                "status" : "success",
                "message" : "retrived",
                "data" : serializer.data
            }, status=status.HTTP_200_OK)
        
        except NotFound as e:
            return Response({
                "status" : "failed",
                "message" : str(e)
            }, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({
                "status" : "failed",
                "message" : "server error",
                "error" : str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)