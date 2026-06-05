"""
Simulate paid users at a fixed interval for local/testing.

Usage:
    python manage.py simulate_payments              # one fake payment every 5s, forever
    python manage.py simulate_payments --interval 2 # every 2 seconds
    python manage.py simulate_payments --count 10   # stop after 10 payments
    python manage.py simulate_payments --clear      # wipe simulated entries first
"""
import time
from uuid import uuid4

from django.core.management.base import BaseCommand
from django.db import transaction

from application.models import UserPreCheckout, PaymentCompleted
from application.messages import random_payment_message


SIM_PREFIX = "sim_"


class Command(BaseCommand):
    help = "Create fake completed payments at a regular interval for testing."

    def add_arguments(self, parser):
        parser.add_argument(
            "--interval",
            type=float,
            default=5.0,
            help="Seconds between fake payments (default: 5).",
        )
        parser.add_argument(
            "--count",
            type=int,
            default=0,
            help="Stop after N payments. 0 = run forever (default).",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete previously-simulated entries before starting.",
        )

    def handle(self, *args, **options):
        interval = options["interval"]
        count = options["count"]
        clear = options["clear"]

        if clear:
            deleted, _ = UserPreCheckout.objects.filter(
                token__startswith=SIM_PREFIX
            ).delete()
            self.stdout.write(self.style.WARNING(
                f"Cleared {deleted} simulated rows."
            ))

        self.stdout.write(self.style.SUCCESS(
            f"Simulating payments every {interval}s "
            f"({'forever' if count == 0 else f'{count} total'}). Ctrl+C to stop."
        ))

        made = 0
        try:
            while count == 0 or made < count:
                self._create_payment()
                made += 1
                self.stdout.write(f"  + payment #{made} created")
                if count == 0 or made < count:
                    time.sleep(interval)
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("\nStopped."))

        self.stdout.write(self.style.SUCCESS(f"Done. Created {made} payments."))

    @transaction.atomic
    def _create_payment(self):
        suffix = uuid4().hex[:12]
        token = f"{SIM_PREFIX}{suffix}"
        pre = UserPreCheckout.objects.create(
            token=token,
            checkout_session_id=f"{SIM_PREFIX}cs_{suffix}",
            message=random_payment_message(),
        )
        PaymentCompleted.objects.create(
            user_pre_checkout=pre,
            stripe_payment_id=f"{SIM_PREFIX}pi_{suffix}",
        )
