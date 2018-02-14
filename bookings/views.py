from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404, HttpResponseRedirect, get_object_or_404, redirect

# Create your views here.
from shops.models import ShopAccount
from bookings.models import Booking
from bookings.forms import BookingForm, BookingUpdateForm
from bookings.mixins import BookingManagerMixin
from notifications.signals import notify


def booking_create_view(request, pk=None):
    if request.method == 'POST':
        print (request.POST)
        # shop_id = request.POST.get('shop')
        instance_location_destination = request.POST.get('instance_location_destination')
        # shop_id_instance = get_object_or_404(ShopAccount, pk=pk)
        # print (shop_id_instance)
        form = BookingForm(request.POST)

        # try:
        #     shop = ShopAccount.objects.get(pk=shop_id)    
        # except Exception as e:
        #     shop = None

        if form.is_valid():
            instance = form.save(commit=False)
            instance.shop = shop_id_instance.business_name
            instance.save()
            # booking_date = form.cleaned_data['booking_date']
            # mobile_contact = form.cleaned_data['mobile_contact']
            # optional_names = form.cleaned_data['optional_names']
            # promotional_code = form.cleaned_data['promotional_code']
            # extra_notes = form.cleaned_data['extra_notes']
            # new_booking = Booking.objects.create_booking(
            # 	user = request.user,
	           #  destination = instance_location_destination,
	           #  # shop = shop,
	           #  booking_date = booking_date,
	           #  mobile_contact = mobile_contact,
	           #  optional_names = optional_names,
	           #  promotional_code = promotional_code,
	           #  extra_notes = extra_notes
            # )
            return HttpResponseRedirect(shop.get_absolute_url())
            messages.success(request, "<strong>Booking</strong> successful ", extra_tags='html_safe')
        else:
            return HttpResponseRedirect(instance_location_destination)
            messages.error(request, "<strong>Oops!</strong>, an error occurred during booking, try again.", extra_tags='html_safe')
    else:
        raise Http404

@login_required
def bookings_detail(request, pk=None):
    obj = get_object_or_404(Booking, pk=pk)
    template = "bookings/detail.html"
    context = {
        "book_object":obj,
    }
    return render(request, template, context)


@login_required
def booking_update(request, pk=None):
    obj = get_object_or_404(Booking, pk=pk)
    booking_form  = BookingUpdateForm(request.POST or None, instance=obj)
    if booking_form.is_valid():
        instance = booking_form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(obj.get_absolute_url())
        messages.success(request, "<strong>Booking Rescheduled</strong> successful ", extra_tags='html_safe')
    template = "bookings/update.html"
    context = {
        "booking_obj":obj,
        "booking_form":booking_form
    }
    return render(request, template, context)