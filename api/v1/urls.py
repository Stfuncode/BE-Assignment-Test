from django.urls import include, path


urlpatterns = [
    # app routes
    path('inventory/', include("inventory.urls")),
]