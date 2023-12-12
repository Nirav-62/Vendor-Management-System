from django.urls import path
from api.views import VendorAPI,obtain_key,PurchaseOrderAPI,PurchaseOrderAcknowledge,showPerformance

urlpatterns = [
    path('vendors/<int:vendor_id>/', VendorAPI.as_view(), name='VendorAPI'),
    path('vendors/', VendorAPI.as_view(), name='VendorAPI'),
    path('vendors/<int:vendor_id>/performance', showPerformance),


    path('purchase_orders/',PurchaseOrderAPI.as_view(),name='PurchaseOrder'),
    path('purchase_orders/<int:po_id>/',PurchaseOrderAPI.as_view(),name='PurchaseOrder'),
    path('purchase_orders/<int:po_id>/acknowledge',PurchaseOrderAcknowledge,name='PurchaseOrderAcknowledge'),


    path('obtain_key/<int:vendor_id>/',obtain_key),
    
]
