from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # template view
    path('inventory/', include('inventory.template_urls')),

    # api view
    path('api/v1/', include('api.v1.urls')),
]
