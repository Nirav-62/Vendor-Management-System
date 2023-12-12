from django.db import models
from django.db.models.signals import post_save,pre_delete
from django.dispatch import receiver
from django.utils import timezone
import uuid



class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(unique=True, max_length=50,blank=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)
    api_key = models.UUIDField(default=uuid.uuid4, editable=False)


    def __str__(self):
        return self.name

@receiver(post_save, sender=Vendor)
def generate_vendor_code_after_save(sender, instance, created, **kwargs):
    if created and not instance.vendor_code:
        if instance.pk is not None:
            instance.vendor_code = f"V-{instance.pk}"
            instance.api_key = uuid.uuid4()
            instance.save()



def default_delivery_date():
    return timezone.now() + timezone.timedelta(days=3)

class PurchaseOrder(models.Model):
    po_number = models.AutoField(primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(default=default_delivery_date)
    items = models.JSONField()
    quantity = models.IntegerField(blank=True,null=True)
    status = models.CharField(max_length=50,default='pending' ,choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ])
    quality_rating = models.FloatField(blank=True , null= True ,default=None)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)




    def __str__(self):
        return f"PO-{self.po_number}"
    
@receiver(post_save, sender=PurchaseOrder)
def calculate_and_store_quantity(sender, instance, **kwargs):  # this function calculate total item quantity given in items fileds and store in quantity field
    # Calculate total quantity
    sum=0
    for item in instance.items:
        sum += item['quantity']
    total_quantity = sum

    # Store the quantity in the instance
    instance.quantity = total_quantity
    PurchaseOrder.objects.filter(pk=instance.pk).update(quantity=total_quantity)


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()
    

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"
