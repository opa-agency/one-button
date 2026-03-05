from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(UserPreCheckout)
class UserPreCheckoutAdmin(admin.ModelAdmin):
	list_display = ("token", "checkout_session_id", "created_at")


@admin.register(PaymentCompleted)
class PaymentCompletedAdmin(admin.ModelAdmin):
	list_display = ("user_pre_checkout", "stripe_payment_id", "created_at")
