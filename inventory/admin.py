from django.contrib import admin

# models
from .models import Inventory, Supplier



admin.site.register(Inventory)
admin.site.register(Supplier)
