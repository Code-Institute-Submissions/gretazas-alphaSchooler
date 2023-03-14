from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem

from products.models import Product
from profiles.models import UserProfile
from bag.contexts import bag_contents
import stripe
import json


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })

        return HttpResponse(status=200)
    except Exception as e:
        print(e)
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    ''' Render checkout page '''

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'country': request.POST['country'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()
            for item_id, item_data in bag.items():
                try:
                    product = Product.objects.get(id=item_id)   
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=item_data,
                    )
                    order_line_item.save()

                except Product.DoesNotExist:
                    messages.error(request, (
                        "Some products in your bag wasn't found in our system."
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))
            request.session['save_info'] = 'save_info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            print(order_form.cleaned_data)
            print(order_form.errors)
            messages.error(request, 'Something went wrong with your form. \
                Please double check your information.')
    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "Your bag is empty")
            return redirect(reverse('products'))

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key

        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.saved_phone_number,
                    'country': profile.saved_country,
                    'postcode': profile.saved_postcode,
                    'town_or_city': profile.saved_town_or_city,
                    'street_address1': profile.saved_street_address1,
                    'street_address2': profile.saved_street_address2,
                    'county': profile.saved_county,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()
    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    # total_user_points = settings.COLLECTED_POINTS + total
    stripe_total = round(total * 100)
    intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
            )

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret
        }

    return render(request, template, context)


def checkout_success(request, order_number):
    """ Handle successful checkouts """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

        # Saved user's info for next time
        if save_info:
            profile_data = {
                'saved_phone_number': order.phone_number,
                'saved_country': order.country,
                'saved_postcode': order.postcode,
                'saved_town_or_city': order.town_or_city,
                'saved_street_address1': order.street_address1,
                'saved_street_address2': order.street_address2,
                'saved_county': order.county,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(request, f'Order successful! \
        Order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')
    points_page = True
    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
