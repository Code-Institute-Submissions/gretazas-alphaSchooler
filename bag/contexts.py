from decimal import Decimal
from django.conf import settings


def bag_contents(request):
    """ View that renders bag contents """

    bag_items = []
    total = 0
    product_count = 0
    collected_points = 0
    use_points = 0
    collected_points_total = settings.COLLECTED_POINTS
    bag = request.session.get('bag', {})
  
    for item_id, item_data in bag.items():
        if isinstance(item_data, int):
            product = get_object_or_404(Product, pk=item_id)
            total += item_data * product.price
            product_count += item_data
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
        else:
            product = get_object_or_404(Product, pk=item_id)
            total += quantity * product.price
            product_count += quantity
            bag_items.append({
                'item_id': item_id,
                'quantity': quantity,
                'product': product,
            })

# Delivery
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDART_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD * total
    else:
        dekivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

# Points
    if use_points:
        collected_money = collected_points_total * settings.ONE_PERCENT
        total = total - collected_money

        # For unused points
        if total < 0:
            collected_points_total = total * 2
        else:
            collected_points_total = collected_points_total - total
    else:
        collected_points_total = collected_points_total + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
        'collected_points': collected_points,
        'collected_points_total': settings.COLLECTED_POINTS,
    }
    return context