from django.contrib import admin

# Register your models here.

from billing.models import Transaction, TransactionBooking

admin.site.register(Transaction)
admin.site.register(TransactionBooking)