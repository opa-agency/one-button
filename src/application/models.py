from django.db import models
import stripe 


class UserPreCheckout(models.Model):
    token = models.CharField(max_length=255, unique=True)
    checkout_session_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.token
        
        
    
class PaymentCompleted(models.Model):
    user_pre_checkout = models.OneToOneField(UserPreCheckout, on_delete=models.CASCADE, related_name="payment_completed")
    stripe_payment_id = models.CharField(max_length=255, unique=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"Payment for token {self.user_pre_checkout.token} with Stripe payment ID {self.stripe_payment_id}"