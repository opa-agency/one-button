from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(UserPreCheckout)
class UserPreCheckoutAdmin(admin.ModelAdmin):
	list_display = ("token", "checkout_session_id", "referral_user", "created_at")
	list_filter = ("referral_user",)


@admin.register(PaymentCompleted)
class PaymentCompletedAdmin(admin.ModelAdmin):
	list_display = ("user_pre_checkout", "referral_user", "stripe_payment_id", "created_at")

	def referral_user(self, obj):
		return obj.user_pre_checkout.referral_user
