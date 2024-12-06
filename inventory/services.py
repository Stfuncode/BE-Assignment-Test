from typing import Optional

# models
from .models import Inventory
from django.db.models import Q, QuerySet

# exceptions
from . import exceptions 


class InventoryService:

    def __init__(self):
        # for injecting dependency
        pass

    def get_inventories(
        self,
        name: Optional[str] = None,
        supplier: Optional[str] = None,
        stock: Optional[int] = None,
        availability: Optional[str] = None
    ) -> QuerySet[Inventory]:

        query = Q()
        
        if name:
            query &= Q(name__icontains=name)

        if supplier:
            query &= Q(supplier__name__icontains=supplier)

        if stock is not None:
            stock = int(stock)
            query &= Q(stock=stock)

        if availability is not None:
            availability = availability.lower() == 'true'
            query &= Q(availability=availability)

        inventory_data = Inventory.objects.select_related('supplier').filter(query)

        if inventory_data.count() == 0:
            raise exceptions.NotFound('inventory data not found')

        return inventory_data

    def get_inventory(self, item_id : int) -> Inventory:
        
        try:
            data = Inventory.objects.select_related('supplier').get(pk=item_id)
        except:
            raise exceptions.NotFound(f'Inventory with id {item_id} not found')

        return data