from uuid import uuid4
from urllib.parse import urlencode
from datetime import timedelta
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseNotAllowed, HttpResponse, JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.templatetags.static import static
from requests import request
from decouple import config
import stripe

from .models import UserPreCheckout, PaymentCompleted
from .forms import PartnerSignUpForm
from .messages import random_payment_message

STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY")
STRIPE_PRICE_ID = config("STRIPE_PRICE_ID")
stripe.api_key = STRIPE_SECRET_KEY

DEFAULT_SHARE_TITLE = "Am văzut statistica. Tu n-ai văzut-o."
DEFAULT_SHARE_DESCRIPTION = "Statistică în timp real. Plătesc 10 lei."
DEFAULT_SHARE_TEXT = "Am văzut statistica. Tu n-ai văzut-o."
OG_IMAGE_VERSION = config("OG_IMAGE_VERSION", default="20260618e")


def _canonical_absolute_url(request, path_or_url):
    configured_base_url = getattr(settings, "BASE_URL", None)
    if configured_base_url:
        parsed = urlparse(path_or_url)
        path = parsed.path or "/"
        query = f"?{parsed.query}" if parsed.query else ""
        fragment = f"#{parsed.fragment}" if parsed.fragment else ""
        return f"{configured_base_url.rstrip('/')}{path}{query}{fragment}"
    return request.build_absolute_uri(path_or_url)


def _share_context(
    request,
    *,
    url="",
    text="",
    title="",
    description="",
):
    share_url = _canonical_absolute_url(request, url or reverse("home"))
    share_text = text or DEFAULT_SHARE_TEXT
    share_title = title or DEFAULT_SHARE_TITLE
    share_description = description or DEFAULT_SHARE_DESCRIPTION
    share_image_url = _canonical_absolute_url(request, static("theme/images/share-card.png"))
    share_story_image_url = _canonical_absolute_url(request, static("theme/images/share-story.png"))
    share_image_url = f"{share_image_url}?v={OG_IMAGE_VERSION}"
    return {
        "share_url": share_url,
        "share_text": share_text,
        "share_data_title": share_title,
        "share_meta_title": share_title,
        "share_meta_description": share_description,
        "share_meta_url": share_url,
        "share_image_url": share_image_url,
        "share_story_image_url": share_story_image_url,
    }


def _referral_user_from_value(value):
    if not value:
        return None
    try:
        user_id = int(value)
    except (TypeError, ValueError):
        return None
    return get_user_model().objects.filter(id=user_id).first()


def _build_success_url(request, token):
    configured_base_url = getattr(settings, "BASE_URL", None)
    if configured_base_url:
        parsed = urlparse(configured_base_url)
        if parsed.scheme and parsed.netloc:
            return f"{configured_base_url.rstrip('/')}{reverse('checkout_finalize')}?{urlencode({'token': token})}"
    return request.build_absolute_uri(
        f"{reverse('checkout_finalize')}?{urlencode({'token': token})}"
    )


def register_view(request):
    if request.user.is_authenticated:
        return redirect("partner_dashboard")

    if request.method == "POST":
        form = PartnerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("partner_dashboard")
    else:
        form = PartnerSignUpForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def partner_dashboard_view(request):
    referral_url = request.build_absolute_uri(
        f"{reverse('home')}?{urlencode({'refferal': request.user.id})}"
    )
    referral_share_text = "Plateste 10 lei prin linkul meu"
    referred_payments = (
        PaymentCompleted.objects.select_related("user_pre_checkout")
        .filter(user_pre_checkout__referral_user=request.user)
        .order_by("-created_at")
    )
    context = {
        "referral_url": referral_url,
        "referral_share_text": referral_share_text,
        "referred_payments": referred_payments,
        "referred_payments_count": referred_payments.count(),
        "referral_total_ron": referred_payments.count(),
    }
    context.update(
        _share_context(
            request,
            url=referral_url,
            text=referral_share_text,
            title="Plătesc 10 Lei — Folosește linkul meu",
            description="Intri direct în statistica live dacă plătești 10 lei prin linkul meu.",
        )
    )
    return render(request, "partner_dashboard.html", context)


def _dashboard_context(
    token_expires_at=None,
    token=None,
    order_number=None,
    share_host="",
    share_url="",
    share_text="",
):
    completed_payments_count = PaymentCompleted.objects.count()
    recent_payments = PaymentCompleted.objects.select_related(
        "user_pre_checkout"
    ).order_by("-created_at")[:8]
    if not share_url and share_host:
        share_url = f"https://{share_host}"
    if not share_text:
        share_text = DEFAULT_SHARE_TEXT
    return {
        "completed_payments_count": completed_payments_count,
        "total_lei": completed_payments_count * 10,
        "token_expires_at": token_expires_at,
        "recent_payments": recent_payments,
        "token": token,
        "order_number": order_number,
        "share_host": share_host,
        "share_url": share_url,
        "share_text": share_text,
    }


def home_page_view(request):
    token = request.GET.get("token") or request.POST.get("token")
    referral_value = (
        request.GET.get("refferal")
        or request.POST.get("refferal")
        or request.GET.get("referral")
        or request.POST.get("referral")
    )
    if request.method == "GET":
        if not token:
            token = uuid4().hex
            query = {"token": token}
            if referral_value:
                query["refferal"] = referral_value
            return redirect(f"/?{urlencode(query)}")
        context = {"token": token, "refferal": referral_value}
        context.update(_share_context(request))
        return render(request, "home.html", context)

    elif request.method == "POST":
        if not token:
            return HttpResponseNotAllowed("No token in query parameter")
        referral_user = _referral_user_from_value(referral_value)
        success_url = _build_success_url(request, token)
        metadata = {"token": token}
        if referral_user:
            metadata["referral_user_id"] = str(referral_user.id)
        stripe_session = stripe.checkout.Session.create(
            success_url=success_url,
            line_items=[{"price": STRIPE_PRICE_ID, "quantity": 1}],
            mode="payment",
            metadata=metadata,
        )

        UserPreCheckout.objects.update_or_create(
            token=token,
            defaults={
                "checkout_session_id": stripe_session.id,
                "referral_user": referral_user,
            },
            create_defaults={
                "checkout_session_id": stripe_session.id,
                "referral_user": referral_user,
                "message": random_payment_message(),
            },
        )

        return redirect(stripe_session.url)


def checkout_finalize_view(request):
    token = request.GET.get("token")
    user_pre_checkout = UserPreCheckout.objects.filter(token=token).first()
    if not user_pre_checkout:
        return HttpResponse("Invalid token")
    session = stripe.checkout.Session.retrieve(user_pre_checkout.checkout_session_id)
    print(f"Stripe session metadata token: {session.metadata.token}")
    payment_status = session.payment_status
    print(f"Stripe session payment status: {payment_status}")
    if payment_status == "paid":
        print("Payment successful!")
        PaymentCompleted.objects.update_or_create(
            user_pre_checkout=user_pre_checkout,
            defaults={"stripe_payment_id": session.payment_intent},
        )
    return redirect(f"{reverse('dashboard')}?{urlencode({'token': token})}")


def dashboard_view(request):
    token = request.GET.get("token") or request.POST.get("token")
    if not token:
        return render(request, "missing_token.html", status=404)

    payment_completed = (
        PaymentCompleted.objects.select_related("user_pre_checkout")
        .filter(user_pre_checkout__token=token)
        .first()
    )
    if not payment_completed:
        return render(request, "invalid_token.html", status=404)

    valid_until = payment_completed.created_at + timedelta(minutes=3)
    if timezone.now() > valid_until:
        return render(request, "expired_token.html", status=410)

    context = _dashboard_context(
        token_expires_at=valid_until.isoformat(),
        token=token,
        order_number=payment_completed.order_number(),
        share_host=request.get_host(),
        share_url=request.build_absolute_uri(reverse("home")),
    )
    context.update(
        _share_context(
            request,
            url=context.get("share_url"),
            text=context.get("share_text"),
        )
    )
    return render(request, "dashboard.html", context)


def dashboard_admin_view(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    if not request.user.is_authenticated:
        return redirect(f"{reverse('login')}?{urlencode({'next': request.path})}")

    context = _dashboard_context(
        share_host=request.get_host(),
        share_url=request.build_absolute_uri(reverse("home")),
    )
    context.update(
        _share_context(
            request,
            url=context.get("share_url"),
            text=context.get("share_text"),
        )
    )
    return render(request, "dashboard.html", context)


def live_stats_view(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    count = PaymentCompleted.objects.count()
    recent = PaymentCompleted.objects.select_related("user_pre_checkout").order_by(
        "-created_at"
    )[:8]
    now = timezone.now()
    latest = []
    for payment in recent:
        created = payment.created_at or now
        latest.append(
            {
                "id": payment.id,
                "order_number": payment.order_number(),
                "message": payment.user_pre_checkout.message,
                "since_seconds": int((now - created).total_seconds()),
            }
        )
    return JsonResponse(
        {
            "count": count,
            "total_lei": count * 10,
            "latest": latest,
        }
    )
