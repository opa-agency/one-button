import hashlib
import hmac
import json
from datetime import datetime, timezone
from urllib.parse import urlsplit
from uuid import uuid4

import requests
from decouple import config


def main() -> None:
    merchant = config("PAYU_MERCHANT_CODE")
    secret = config("PAYU_SECRET_KEY")
    endpoint = "https://secure.payu.ro/api/v4/payments/authorize"

    payload = {
        "merchantPaymentReference": f"payref-{uuid4()}",
        "currency": "RON",
        "returnUrl": "https://example.com/confirm",
        "authorization": {"paymentMethod": "CCVISAMC", "usePaymentPage": "YES"},
        "client": {
            "billing": {
                "firstName": "John",
                "lastName": "Doe",
                "email": "john.doe@example.com",
                "countryCode": "RO",
                "phone": "0712345678",
            }
        },
        "products": [{"name": "Test product", "sku": "SKU-1", "unitPrice": 10, "quantity": 1}],
    }

    body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    date_header = datetime.now(timezone.utc).isoformat(timespec="seconds")
    parsed = urlsplit(endpoint)
    signature_payload = (
        f"{merchant}{date_header}POST{parsed.path}{parsed.query}{hashlib.md5(body).hexdigest()}"
    )
    signature = hmac.new(secret.encode(), signature_payload.encode(), hashlib.sha256).hexdigest()

    response = requests.post(
        endpoint,
        data=body,
        timeout=30,
        headers={
            "Content-Type": "application/json",
            "X-Header-Merchant": merchant,
            "X-Header-Date": date_header,
            "X-Header-Signature": signature, 
        },
    )
    response.raise_for_status()
    print(response.json().get("authorization", {}).get("url"))


if __name__ == "__main__":
    main()
