from rest_framework import serializers

# models
from .models import Inventory, Supplier



class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        exclude = ['updated_at', 'created_at']

class InventorySerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer()

    class Meta:
        model = Inventory
        exclude = ['updated_at', 'created_at']