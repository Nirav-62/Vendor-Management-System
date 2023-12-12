from django.db.models.signals import post_save, pre_delete,pre_save
from django.dispatch import receiver
from django.db.models import Avg, F
from api.models import PurchaseOrder, Vendor ,HistoricalPerformance
from django.utils import timezone





def save_historical_performance(vendor, on_time_delivery_rate, quality_rating_avg, response_times, fulfilment_rate):
    HistoricalPerformance.objects.create(
        vendor=vendor,
        date=timezone.now(),
        on_time_delivery_rate=on_time_delivery_rate,
        quality_rating_avg=quality_rating_avg,
        average_response_time=response_times,
        fulfillment_rate=fulfilment_rate,
    )


@receiver(post_save, sender=PurchaseOrder)
def calculate_on_time_delivery_rate(sender, instance, created, **kwargs):
    # print("start function")
    if  instance.status == 'completed' and instance.delivery_date and instance.acknowledgment_date is not None:
        total_completed_orders = PurchaseOrder.objects.filter(vendor=instance.vendor, status='completed').count()
        
        # print("in function total_completed_orders ",total_completed_orders)

        if total_completed_orders > 0 and instance.acknowledgment_date <= instance.delivery_date:
            on_time_deliveries = PurchaseOrder.objects.filter(
                vendor=instance.vendor,
                status='completed',
                delivery_date__gte=F('acknowledgment_date')
            ).count()
            # print("on_time_deliveries : ",on_time_deliveries)
            on_time_delivery_rate = (on_time_deliveries / total_completed_orders) * 100
            # print("on_time_deliveries rate: ",on_time_delivery_rate)

            # Update Vendor's On-Time Delivery Rate
            Vendor.objects.update_or_create(
                pk=instance.vendor.pk,
                defaults={'on_time_delivery_rate': on_time_delivery_rate}
            )
            save_historical_performance(instance.vendor,on_time_delivery_rate,instance.vendor.quality_rating_avg ,instance.vendor.average_response_time,instance.vendor.fulfillment_rate)

            
        else:
            # No completed orders for the vendor or acknowledgment date is later than delivery date
            Vendor.objects.update_or_create(
                pk=instance.vendor.pk,
                defaults={'on_time_delivery_rate': 2.2}
            )
    # print("end function did nothing")










# Signal for Quality Rating Average
@receiver(post_save, sender=PurchaseOrder)
def calculate_quality_rating_average(sender, instance, created, **kwargs):   # Here we are not uisng created because quality rating is given after the order is delivered or completed
#    print("in calculate_quality_rating_average function")
   if  instance.quality_rating is not None:
        # Calculate Quality Rating Average
        completed_orders = PurchaseOrder.objects.filter(
            vendor=instance.vendor,
            status='completed',
            quality_rating__isnull=False
        )
        # print("in depth calculate_quality_rating_average function")

        if completed_orders.exists():
            quality_rating_avg = completed_orders.aggregate(Avg('quality_rating'))['quality_rating__avg']
            quality_rating_avg_proper = round(quality_rating_avg, 3)
            
            Vendor.objects.update_or_create(
                pk=instance.vendor.pk,
                defaults={'quality_rating_avg': quality_rating_avg_proper}
            )
            save_historical_performance(instance.vendor,instance.vendor.on_time_delivery_rate,quality_rating_avg_proper ,instance.vendor.average_response_time,instance.vendor.fulfillment_rate)

        else:
            # No completed orders with quality ratings for the vendor, set quality_rating_avg to 0.0
            Vendor.objects.update_or_create(
                pk=instance.vendor.pk,
                defaults={'quality_rating_avg': 0.0}
            )

    
        

# Signal for Average Response Time

def calculate_average_response_time_fun(orders):
    """
    Calculates the average response time for a list of purchase orders.
    """
    # print("start for calculating response function")

    total_response_time_hours = 0
    valid_orders = 0

    for order in orders:
        if order.acknowledgment_date is not None and order.issue_date is not None:
            response_time_hours = (order.acknowledgment_date - order.issue_date).total_seconds() / 3600
            total_response_time_hours += response_time_hours
            valid_orders = len(orders)
            # print("for calculating calculate_average_response_time_fun function")
    if valid_orders > 0:
        average_response_time = total_response_time_hours / valid_orders
        print(average_response_time)
    else:
        average_response_time = None

    return average_response_time
@receiver(post_save , sender=PurchaseOrder)
def calculate_average_response_time(sender, instance, created, **kwargs):


    if instance.acknowledgment_date is not None:
        orders = PurchaseOrder.objects.filter(
            vendor=instance.vendor,
            acknowledgment_date__isnull=False,
            issue_date__isnull=False
        )
        print("in calculate_average_response_time  function")

        avg_response_time = calculate_average_response_time_fun(orders)
        print(avg_response_time)
        avg_response_time_rounded = round(avg_response_time , 3)
        Vendor.objects.update_or_create(
            pk=instance.vendor.pk,
            defaults={'average_response_time': avg_response_time_rounded})
        save_historical_performance(instance.vendor,instance.vendor.on_time_delivery_rate,instance.vendor.quality_rating_avg ,avg_response_time_rounded,instance.vendor.fulfillment_rate)

        print("complete calculate_average_response_time function")
    
orders = PurchaseOrder.objects.filter(
            vendor=4,
            acknowledgment_date__isnull=False,
            issue_date__isnull=False
        )


@receiver(pre_delete, sender=PurchaseOrder)
def calculate_fulfilment_rate(sender, instance, **kwargs):
    # Calculate Fulfilment Rate
    total_orders = PurchaseOrder.objects.filter(vendor=instance.vendor).count()
    successful_orders = PurchaseOrder.objects.filter(
        vendor=instance.vendor,
        status='completed'
    ).count()

    fulfilment_rate = (successful_orders / total_orders) * 100 if total_orders > 0 else 0.0

    # Update Vendor's Fulfilment Rate
    Vendor.objects.filter(pk=instance.vendor.pk).update(fulfillment_rate=fulfilment_rate)
    save_historical_performance(instance.vendor,instance.vendor.on_time_delivery_rate,instance.vendor.quality_rating_avg ,instance.vendor.average_response_time,fulfilment_rate)
