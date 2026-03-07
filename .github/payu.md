openapi: 3.0.0
info:
  description: |
    <a href="/docs/old">Go to old APIs</a>

    This collection of APIs is used to interact with PayU for processing payments.
    Please be aware that some options are available:
    - per platform. This API collection is suitable for using PayU in Romania.
    - per merchant. It might need to be setup by our operational team.
    - per payment processor. We integrate with many payment processors, and not all support the same features.

    # Overview

      These APIs will allow a merchant to accept online payments on its website. There are multiple payment flows a merchant can integrate.
      For the normal payment flow, use [Payment API](#tag/Payment-API).
      For other payment flows, continue reading.

      ## API Evolution & Extensibility
      The APIs HTTP responses and webhooks HTTP requests are designed to be forward compatible.
      This means that additional fields may be added in the future to support new features.<br/>
      <strong>Clients are expected to ignore any unknown fields, ensuring that these additive changes do not break existing integrations.</strong>
      This design follows the [Tolerant Reader](https://martinfowler.com/bliki/TolerantReader.html) pattern, in line with the [robustness principle](https://en.wikipedia.org/wiki/Robustness_principle), "*be conservative in what you send, be liberal in what you accept*".

      ## Marketplace payment flow

        This is a payment flow that allows the merchant to enhance the normal payment flow.<br/>
        In order to use the Marketplace Payment Flow, you'll make use of [Marketplace APIs](#tag/Marketplace-API), along with the [Payment APIs](#tag/Payment-API). <br/>
        What this payment flow changes in how you use Payment API is that it adds additional nodes with information. These additional nodes will be marked in our documentation. <br/>
        Some of this information will be set by the merchant, while some will be information generated through [Marketplace APIs](#tag/Marketplace-API)

    # Old documentation

    **<a href="old">Go to old API documentation</a>**

    # Secure Fields

    **<a href="secure-fields/">Go to Secure Fields documentation</a>**

    # Testing

    You can use [Postman](https://www.getpostman.com/) to test our APIs.
    Bellow there is a postman collection that will help you test main flows:

    <table>
      <tr>
        <td><strong>Description</strong></td>
        <td><strong>Postman files<strong></td>
      </tr>
      <tr>
        <td>A collection of all available APIs including also some specific business flows</strong></td>
        <td>
          <a href="swagger/postman/PayU-Standard.postman_collection.json">PayU APIs</a> |
          <a href="swagger/postman/PayU-Standard_RO.postman_environment.json">Env</a>
        </td>
      </tr>
    </table>
    Current environment files are setup with some general accounts and data can be removed at any time.<br/>
    On any environment you can replace `PAYU_SECRET_KEY` and `PAYU_MERCHANT_CODE` with the one provided by our integration team.


    # Idempotent Requests
    API supports idempotency

    ## How does it work:
    The API supports idempotency for safely retrying requests without accidentally performing the same operation twice.
    <br/>

     Idempotency works by saving the response of the requests for 24 hours, during which time clients can use same idempotency key to retrive the original response. Making multiple identical requests has the same effect as making a single request </br>
     You can use same Idempotency key 24 hour, after that the key will be deleted.

    All POST requests accept idempotency keys. Sending idempotency keys in GET and DELETE requests has no effect and should be avoided.

     ## Idempotency key are provide in headers bellow:

    <table>
      <tr>
        <td><strong>Header</strong></td>
        <td><strong>Description<strong></td>
      </tr>
      <tr>
        <td>X-Header-Idempotency-Key</strong></td>
        <td>Any non-empty string with max length 36 characters</td>
      </tr>
    </table>
    &nbsp;



    # API Limits
    There are some API limits in place.

    ## How does it work:
    In order to avoid an unreasonable number of requests from one merchant, some PayU APIs are protected by a quota-system that allows only a certain number of requests during a period of 60 seconds.
    The APIs that are protected by this system will send additional response headers, so the consumer application knows how many requests it has left.
    If the merchant exceeds his quota, he will have to wait before making anymore requests to that API

    ## API Limits are provide in headers bellow:

     <table>
      <tr>
        <td><strong>Header</strong></td>
        <td><strong>Description<strong></td>
      </tr>
      <tr>
        <td>X-Rate-Limit-Limit</strong></td>
        <td>Number of allowed requests for a period of 60 seconds</td>
      </tr>
      <tr>
        <td>X-Rate-Limit-Reset</strong></td>
        <td>How much time remains, in seconds, until the end of the current period of 60 seconds</td>
      </tr>
      <tr>
        <td>X-Rate-Limit-Remaining</strong></td>
        <td>Requests available until the end of current period of 60 seconds</td>
      </tr>
    </table>
    &nbsp;

    ## Exceeding requests quota
    When client exceeds requests quota, server will return response code 429 (Too Many Requests)

    # Authentication

    All requests performed to our endpoints must include a computed signature, otherwise they will fail.
    The signature is passed in the request's `X-Header-Signature` header. The following headers must be sent as well:

  version: "4.0.0"
  title: API V4

  x-logo:
    url: /images/epayment.jpg

tags:
  - name: Marketplace API
    description: APIs used in order to use Marketplace Payment Flow
  - name: Payment API
    description: Payment API V4. If your integration is using API V2, <a href="/docs/api-migration/payments/">go to migration guide</a>.
  - name: Payouts API
    description: This API allows a merchant to make transfers using a card or a token. He can also retrieve info about past payouts or the current payout balance.
  - name: Webhooks
    description: |
      Structure of notifications sent by PayU for different payment flows. 

      If your integration is using the old IPN API, <a href="/docs/api-migration/ipn/">go to migration guide</a>.
      
      PayU sends webhook notifications to merchants’ systems as part of various payment flows.
      To ensure these notifications are delivered successfully, especially in environments protected by firewalls or IP whitelisting rules, it is important to allow incoming traffic from the following trusted IP addresses used by PayU.

      | Environment | IP Addresses |
      |-------------|--------------|
      | **Production** | `185.68.12.10`  <br/> `185.68.12.11` <br/> `185.68.12.12` <br/> `185.68.12.26` <br/> `185.68.12.27` <br/> `185.68.12.28` <br/> `185.68.14.6` |
      | **Sandbox**    | `185.68.14.85` <br/> `185.68.14.1` |
      > ⚠️ **Important:** These IPs should be whitelisted by merchants in order to ensure proper delivery of notifications in both production and sandbox environments.
      
      These IPs are shown here for informative purposes, in case you consider adding a second layer of security on top of the one described in the "Authentication" section, or a whitelisting is required.

      Even so, the primary security mechanism should still be the one described in the "Authentication" section, meaning that you should always check the signature of the request you receive from our systems.
  - name: Token API
    description: |
      This API can create tokens associated with buyer's cards, delete or get info for existing tokens. If your integration is using API V2, <a href="/docs/api-migration/token/">go to migration guide</a>.
      
      The token is a cryptographically secure random value which should be stored securely. 
              Later, it can be used to authorize further transactions with the same card that was initially tokenized.
  - name: CardInfo API
    description: This API allows a merchant to retrieve card information using a card bin or a token. If your integration is using API V2, <a href="/docs/api-migration/cardinfo/">go to migration guide</a>.
  - name: Automatic OnBoarding Api
    description: |
      **Automatic OnBoarding Api - Old documentation:
      <a href="onboarding">Go to Automatic OnBoarding Api - Old documentation</a>**
  - name:  Reports API
    description: |
       **This api hasn't been migrated to this version, please use the old version from here:
       <a href="old/reports">Go to Reports API documentation</a>**
  - name: Merchant Transfers API
    description: |
        **This api hasn't been migrated to this version, please use the old version from here:
        <a href="old/transfers">Go to Merchant Transfers API documentation</a>**
  - name: FX API
    description: The FX feature allows for completing payments by using different currencies than the order's currency, converting the total price to buyer's own card currency. If your integration is using API V2 <a href="old/fx">Go to FX API documentation</a>
#  - name: Secure Fields API
#    description: |
#        # Using the Secure Fields Form
#        The Secure Fields Form is an HTML form that you can include in your site to collect a user’s card information
#        When card information is submitted through the Secure Fields Form, PayU returns a token representation of the card to your site.
#        If you added additional fields to the form, then these fields are included in the token representation of the card as well.
#        You must use the token when <a href="#tag/Payment-API/paths/~1v4~1payments~1authorize/post">create and authorize a payment.
#        ### <a href="secure-fields">Go to Secure fields documentation</a>
  - name: Sessions
    description: This API allows a merchant to create a <strong>sessionId</strong> to be further used when <a href="#tag/Payment-API/paths/~1v4~1payments~1authorize/post"> authorizing a payment</a> with oneTimeUseToken.
  - name: Merchant API
    description: This API allows a payment facilitator to create a merchant. It will be accessible only for payment facilitators, not also for regular merchants.
  - name: Response codes
    # https://redocly.com/docs-legacy/api-reference-docs/guides/embedded-markdown
    # ReDoc enables you to embed external Markdown file contents into description fields
    # noinspection YAMLSchemaValidation
    description:
      $ref: './authorization_response_codes.md'

servers:
- description: Url
  url: 'https://secure.payu.ro/api'

paths:
  /v4/payments/authorize:
    parameters:
    - $ref: '#/components/parameters/X-Header-Signature'
    - $ref: '#/components/parameters/X-Header-Merchant'
    - $ref: '#/components/parameters/X-Header-Submerchant-Id'
    - $ref: '#/components/parameters/X-Header-Date'
    - $ref: '#/components/parameters/X-Header-Idempotency-Key'
    post:
      tags:
       - Payment API
      description: "Create and authorize a payment"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              oneOf:
                - $ref: '#/components/schemas/Payment_with_payment_page'
                - $ref: '#/components/schemas/Payment_with_direct_card'
                - $ref: '#/components/schemas/Payment_with_merchant_token'
                - $ref: '#/components/schemas/Payment_with_network_token'
                - $ref: '#/components/schemas/Payment_with_google_pay_token'
                - $ref: '#/components/schemas/Payment_with_apple_pay_token'
                - $ref: '#/components/schemas/Payment_with_one_time_use_token'
                - $ref: '#/components/schemas/Payment_with_BT24_internet_banking'
                - $ref: '#/components/schemas/Payment_with_wire_transfer'
                - $ref: '#/components/schemas/Payment_with_open_banking'
                - $ref: '#/components/schemas/Payment_with_btpay'

      responses:
        '200':
          description: "Successfully created a payment"
          headers:
            'X-Rate-Limit-Limit':
              $ref: '#/components/headers/X-Rate-Limit-Limit'
            'X-Rate-Limit-Reset':
              $ref: '#/components/headers/X-Rate-Limit-Reset'
            'X-Rate-Limit-Remaining':
              $ref: '#/components/headers/X-Rate-Limit-Remaining'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AuthorizeResponse'
        '4XX':
          description: "Payment failed due to some invalid parameters."
          headers:
            'X-Rate-Limit-Limit':
              $ref: '#/components/headers/X-Rate-Limit-Limit'
            'X-Rate-Limit-Reset':
              $ref: '#/components/headers/X-Rate-Limit-Reset'
            'X-Rate-Limit-Remaining':
              $ref: '#/components/headers/X-Rate-Limit-Remaining'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AluClientErrorsResponse'
        '5XX':
          description: "Payment failed due to some internal errors. Please retry later."
          headers:
            'X-Rate-Limit-Limit':
              $ref: '#/components/headers/X-Rate-Limit-Limit'
            'X-Rate-Limit-Reset':
              $ref: '#/components/headers/X-Rate-Limit-Reset'
            'X-Rate-Limit-Remaining':
              $ref: '#/components/headers/X-Rate-Limit-Remaining'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ServerErrorsResponse'
        '429':
          $ref: '#/components/responses/TooManyRequestResponse'

  /v4/payments/capture:
    parameters:
    - $ref: '#/components/parameters/X-Header-Signature'
    - $ref: '#/components/parameters/X-Header-Merchant'
    - $ref: '#/components/parameters/X-Header-Submerchant-Id'
    - $ref: '#/components/parameters/X-Header-Date'
    - $ref: '#/components/parameters/X-Header-Idempotency-Key'

    post:
      tags:
       - Payment API
      description: "Capture a payment"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CaptureRequest'
      responses:
        '200':
          description: "Successfully send capture request. It will be process according to merchant setup in PayU"
          headers:
            'X-Rate-Limit-Limit':
              $ref: '#/components/headers/X-Rate-Limit-Limit'
            'X-Rate-Limit-Reset':
              $ref: '#/components/headers/X-Rate-Limit-Reset'
            'X-Rate-Limit-Remaining':
              $ref: '#/components/headers/X-Rate-Limit-Remaining'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ConfirmSuccessStatusResponse'
        '4XX':
          description: "Capture failed due to invalid parameters."
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/IdnClientErrorsStatusResponse'
        '5XX':
          description: "Capture failed due to some internal errors. Please retry later."
          headers:
            'X-Rate-Limit-Limit':
              $ref: '#/components/headers/X-Rate-Limit-Limit'
            'X-Rate-Limit-Reset':
              $ref: '#/components/headers/X-Rate-Limit-Reset'
            'X-Rate-Limit-Remaining':
              $ref: '#/components/headers/X-Rate-Limit-Remaining'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/IdnServerErrorsStatusResponse'
        '429':
          $ref: '#/components/responses/TooManyRequestResponse'

  /v4/payments/refund:
    parameters:
    - $ref: '#/components/parameters/X-Header-Signature'
    - $ref: '#/components/parameters/X-Header-Merchant'
    - $ref: '#/components/parameters/X-Header-Submerchant-Id'
    - $ref: '#/components/parameters/X-Header-Date'
    - $ref: '#/components/parameters/X-Header-Idempotency-Key'

    post:
      tags:
       - Payment API
      description: "Refund a payment"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RefundRequest'
      responses:
        '200':
          description: "Successfully send refund request."
          headers:
            'X-Rate-Limit-Limit':
              $ref: '#/components/headers/X-Rate-Limit-Limit'
            'X-Rate-Limit-Reset':
              $ref: '#/components/headers/X-Rate-Limit-Reset'
            'X-Rate-Limit-Remaining':
              $ref: '#/components/headers/X-Rate-Limit-Remaining'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/RefundSuccessStatusResponse'
        '202':
          description: "Place of refund failed due to already cancelled sale"
          headers:
            'X-Rate-Limit-Limit':
              $ref: '#/components/headers/X-Rate-Limit-Limit'
            'X-Rate-Limit-Reset':
              $ref: '#/components/headers/X-Rate-Limit-Reset'
            'X-Rate-Limit-Remaining':
              $ref: '#/components/headers/X-Rate-Limit-Remaining'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/IrnClientAlreadyAuthStatusResponse'
        '4XX':
          description: "Place of refund failed due to invalid parameters"
          headers:
            'X-Rate-Limit-Limit':
              $ref: '#/components/headers/X-Rate-Limit-Limit'
            'X-Rate-Limit-Reset':
              $ref: '#/components/headers/X-Rate-Limit-Reset'
            'X-Rate-Limit-Remaining':
              $ref: '#/components/headers/X-Rate-Limit-Remaining'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/IrnClientErrorsStatusResponse'
        '5XX':
          description: "Refund request failed due to some internal errors. Please retry later."
          headers:
            'X-Rate-Limit-Limit':
              $ref: '#/components/headers/X-Rate-Limit-Limit'
            'X-Rate-Limit-Reset':
              $ref: '#/components/headers/X-Rate-Limit-Reset'
            'X-Rate-Limit-Remaining':
              $ref: '#/components/headers/X-Rate-Limit-Remaining'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/IrnServerErrorsStatusResponse'
        '429':
          $ref: '#/components/responses/TooManyRequestResponse'

  '/v4/payments/status/{merchantPaymentReference}':
      parameters:
        - $ref: '#/components/parameters/X-Header-Signature'
        - $ref: '#/components/parameters/X-Header-Merchant'
        - $ref: '#/components/parameters/X-Header-Submerchant-Id'
        - $ref: '#/components/parameters/X-Header-Date'
        - $ref: '#/components/parameters/merchantPaymentReference'

      get:
        tags:
         - Payment API
        description: Status of a payment
        responses:
          '200':
            description: Successfully get payment status.
            headers:
              X-Rate-Limit-Limit:
                $ref: '#/components/headers/X-Rate-Limit-Limit'
              X-Rate-Limit-Reset:
                $ref: '#/components/headers/X-Rate-Limit-Reset'
              X-Rate-Limit-Remaining:
                $ref: '#/components/headers/X-Rate-Limit-Remaining'
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/StatusSuccessResponse'
          '404':
            description: Payment not found
            headers:
              X-Rate-Limit-Limit:
                $ref: '#/components/headers/X-Rate-Limit-Limit'
              X-Rate-Limit-Reset:
                $ref: '#/components/headers/X-Rate-Limit-Reset'
              X-Rate-Limit-Remaining:
                $ref: '#/components/headers/X-Rate-Limit-Remaining'
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/NotFoundResponse'
          '429':
            $ref: '#/components/responses/TooManyRequestResponse'
          '5XX':
            description: >-
              Refund request failed due to some internal errors. Please retry
              later.
            headers:
              X-Rate-Limit-Limit:
                $ref: '#/components/headers/X-Rate-Limit-Limit'
              X-Rate-Limit-Reset:
                $ref: '#/components/headers/X-Rate-Limit-Reset'
              X-Rate-Limit-Remaining:
                $ref: '#/components/headers/X-Rate-Limit-Remaining'
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/ServerErrorsResponse'

  /v4/merchants:
    post:
      parameters:
        - $ref: '#/components/parameters/X-Header-Signature'
        - $ref: '#/components/parameters/X-Header-Merchant'
        - $ref: '#/components/parameters/X-Header-Date'
      tags:
        - Merchant API
      summary: 'Create merchant for payment facilitator'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/MerchantCreateRequest'
      responses:
        '200':
          $ref: '#/components/responses/200MerchantCreate'
        '400':
          $ref: '#/components/responses/4xxResponse'
        '500':
          $ref: '#/components/responses/5xxResponse'

  /v4/payout:
    post:
      parameters:
        - $ref: '#/components/parameters/X-Header-Signature'
        - $ref: '#/components/parameters/X-Header-Merchant'
        - $ref: '#/components/parameters/X-Header-Date'
        - $ref: '#/components/parameters/X-Header-Idempotency-Key'
      tags:
        - Payouts API
      summary: 'Create payout'
      description: 'Creates a payout request'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PayoutRequest'
      responses:
        '200':
          description: "Successfully sent payout request."
          headers:
            'X-Header-Signature':
              $ref: '#/components/headers/X-Header-Signature'
            'X-Header-Merchant':
              $ref: '#/components/headers/X-Header-Merchant'
            'X-Header-Date':
              $ref: '#/components/headers/X-Header-Date'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PayoutSuccessResponse'
        '4XX':
          description: "Invalid payout request"
          headers:
            'X-Header-Signature':
              $ref: '#/components/headers/X-Header-Signature'
            'X-Header-Merchant':
              $ref: '#/components/headers/X-Header-Merchant'
            'X-Header-Date':
              $ref: '#/components/headers/X-Header-Date'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PayoutClientErrorResponse'
        '401':
          description: "Unauthorized request"
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PayoutUnauthorizedResponse'
        '429':
          description: "Too many requests"
          headers:
            'X-Header-Signature':
              $ref: '#/components/headers/X-Header-Signature'
            'X-Header-Merchant':
              $ref: '#/components/headers/X-Header-Merchant'
            'X-Header-Date':
              $ref: '#/components/headers/X-Header-Date'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PayoutTooManyRequestResponse'
        '5XX':
          description: "Internal server error"
          headers:
            'X-Header-Signature':
              $ref: '#/components/headers/X-Header-Signature'
            'X-Header-Merchant':
              $ref: '#/components/headers/X-Header-Merchant'
            'X-Header-Date':
              $ref: '#/components/headers/X-Header-Date'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PayoutServerErrorsResponse'
        '502':
          description: "Bad gateway"
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BadGatewayResponse'
    get:
      tags:
        - Payouts API
      summary: 'Retrieve payouts'
      description: |
        Retrieves a collection of payouts based on the filters received. Filters are expected as query parameters and we have the available ones listed below. <br/>
        We have a limit on each call to return maximum 50 payouts. <br/>
        To retrieve all the payouts that meet the conditions, you have to continue to call the API using the next url provided in _links node from response (for more details, you can check the response structure below).
      parameters:
        - $ref: '#/components/parameters/X-Header-Signature'
        - $ref: '#/components/parameters/X-Header-Merchant'
        - $ref: '#/components/parameters/X-Header-Date'
        - name: merchantCodes
          in: query
          description: Array of merchant codes
          schema:
            type: array
            items:
              $ref: '#/components/schemas/MerchantCode'
        - name: startDate
          in: query
          description: The start date and time for the range to show in the response. It should be in ISO_8601 Y-m-d\TH:i:sP format (https://en.wikipedia.org/wiki/ISO_8601)
          schema:
            $ref: '#/components/schemas/PayoutHistoryStartDate'
        - name: endDate
          in: query
          description: The end date and time for the range to show in the response. It should be in ISO_8601 Y-m-d\TH:i:sP format (https://en.wikipedia.org/wiki/ISO_8601)
          schema:
            $ref: '#/components/schemas/PayoutHistoryEndDate'
        - name: page
          in: query
          description: 'The page number indicating which set of items will be returned in the response.'
          schema:
            $ref: '#/components/schemas/PayoutHistoryPagination'
      responses:
        '200':
          description: "Payout collection successfully fetched"
          headers:
            'X-Header-Signature':
              $ref: '#/components/headers/X-Header-Signature'
            'X-Header-Merchant':
              $ref: '#/components/headers/X-Header-Merchant'
            'X-Header-Date':
              $ref: '#/components/headers/X-Header-Date'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PayoutHistorySuccessResponse'
        '4XX':
          description: "Invalid request"
          headers:
            'X-Header-Signature':
              $ref: '#/components/headers/X-Header-Signature'
            'X-Header-Merchant':
              $ref: '#/components/headers/X-Header-Merchant'
            'X-Header-Date':
              $ref: '#/components/headers/X-Header-Date'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PayoutHistoryClientErrorResponse'
        '401':
          description: "Unauthorized request"
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PayoutUnauthorizedResponse'
        '429':
          description: "Too many requests"
          headers:
            'X-Header-Signature':
              $ref: '#/components/headers/X-Header-Signature'
            'X-Header-Merchant':
              $ref: '#/components/headers/X-Header-Merchant'
            'X-Header-Date':
              $ref: '#/components/headers/X-Header-Date'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PayoutTooManyRequestResponse'
        '5XX':
          description: "Internal server error"
          headers:
            'X-Header-Signature':
              $ref: '#/components/headers/X-Header-Signature'
            'X-Header-Merchant':
              $ref: '#/components/headers/X-Header-Merchant'
            'X-Header-Date':
              $ref: '#/components/headers/X-Header-Date'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PayoutServerErrorsResponse'
        '502':
          description: "Bad gateway"
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BadGatewayResponse'

  /v4/payout/balance:
    parameters:
      - $ref: '#/components/parameters/X-Header-Signature'
      - $ref: '#/components/parameters/X-Header-Merchant'
      - $ref: '#/components/parameters/X-Header-Date'
    get:
      tags:
        - Payouts API
      summary: 'Get payout balance'
      description: 'Get balance request'
      parameters:
        - name: merchantCodes
          in: query
          description: Array of merchant codes
          required: false
          schema:
            type: array
            items:
              $ref: '#/components/schemas/MerchantCode'
        - name: minValue
          in: query
          description: Minimum balance amount. Need to be provided with `currency`
          schema:
            $ref: '#/components/schemas/BalanceMinAmount'
        - name: maxValue
          in: query
          description: Maximum balance amount. Need to be provided with `currency`
          schema:
            $ref: '#/components/schemas/BalanceMaxAmount'
        - name: currency
          in: query
          description: 'The currency code in which the prices are expressed. According to ISO 4217 (https://en.wikipedia.org/wiki/ISO_4217)'
          schema:
            $ref: '#/components/schemas/Currency'
      responses:
        '200':
          description: "Balance successfully fetched"
          headers:
            'X-Header-Signature':
              $ref: '#/components/headers/X-Header-Signature'
            'X-Header-Merchant':
              $ref: '#/components/headers/X-Header-Merchant'
            'X-Header-Date':
              $ref: '#/components/headers/X-Header-Date'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PayoutBalanceSuccessResponse'
        '4XX':
          description: "Invalid balance request"
          headers:
            'X-Header-Signature':
              $ref: '#/components/headers/X-Header-Signature'
            'X-Header-Merchant':
              $ref: '#/components/headers/X-Header-Merchant'
            'X-Header-Date':
              $ref: '#/components/headers/X-Header-Date'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BalanceClientErrorResponse'
        '401':
          description: "Unauthorized request"
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PayoutUnauthorizedResponse'
        '429':
          description: "Too many requests"
          headers:
            'X-Header-Signature':
              $ref: '#/components/headers/X-Header-Signature'
            'X-Header-Merchant':
              $ref: '#/components/headers/X-Header-Merchant'
            'X-Header-Date':
              $ref: '#/components/headers/X-Header-Date'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PayoutTooManyRequestResponse'
        '5XX':
          description: "Internal server error"
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PayoutServerErrorsResponse'
        '502':
          description: "Bad gateway"
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BadGatewayResponse'

  /v4/marketplace/sellers:
    parameters:
    - $ref: '#/components/parameters/X-Header-Signature'
    - $ref: '#/components/parameters/X-Header-Merchant'
    - $ref: '#/components/parameters/X-Header-Date'
    post:
      tags:
       - Marketplace API
      summary: "Create seller"
      parameters:
      - $ref: '#/components/parameters/X-Header-Idempotency-Key'
      description: "Create a new marketplace seller"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/MarketplaceSellerRequest'

      responses:
        '200':
          description: "Successfully created a new marketplace seller. Id of the created seller will be returned in response for future payments."
          headers:
            'X-Rate-Limit-Limit':
              $ref: '#/components/headers/X-Rate-Limit-Limit'
            'X-Rate-Limit-Reset':
              $ref: '#/components/headers/X-Rate-Limit-Reset'
            'X-Rate-Limit-Remaining':
              $ref: '#/components/headers/X-Rate-Limit-Remaining'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MarketplaceSellerResponse'

        '4XX':
          description: "Create seller failed due to some invalid parameters."
          headers:
            'X-Rate-Limit-Limit':
              $ref: '#/components/headers/X-Rate-Limit-Limit'
            'X-Rate-Limit-Reset':
              $ref: '#/components/headers/X-Rate-Limit-Reset'
            'X-Rate-Limit-Remaining':
              $ref: '#/components/headers/X-Rate-Limit-Remaining'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ClientErrorsResponse'
        '5XX':
          description: "Create seller failed due to some internal errors. Please retry later.."
          headers:
            'X-Rate-Limit-Limit':
              $ref: '#/components/headers/X-Rate-Limit-Limit'
            'X-Rate-Limit-Reset':
              $ref: '#/components/headers/X-Rate-Limit-Reset'
            'X-Rate-Limit-Remaining':
              $ref: '#/components/headers/X-Rate-Limit-Remaining'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ServerErrorsResponse'
    get:
      tags:
        - Marketplace API
      summary: "Get sellers"
      description: "Return the seller list of the current merchant"
      parameters:
        - name: page
          in: query
          description: Number of page
          required: false
          schema:
            type: integer
            example: 1
        - name: pageSize
          in: query
          description: Number of results to be returned
          required: false
          schema:
            type: integer
            example: 1000
      responses:
        '200':
          description: "Successfully retrieved marketplace sellers."
          headers:
            'X-Rate-Limit-Limit':
              $ref: '#/components/headers/X-Rate-Limit-Limit'
            'X-Rate-Limit-Reset':
              $ref: '#/components/headers/X-Rate-Limit-Reset'
            'X-Rate-Limit-Remaining':
              $ref: '#/components/headers/X-Rate-Limit-Remaining'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MarketplaceSellersResponse'

        '4XX':
          description: "Get seller failed due to invalid parameters."
          headers:
            'X-Rate-Limit-Limit':
              $ref: '#/components/headers/X-Rate-Limit-Limit'
            'X-Rate-Limit-Reset':
              $ref: '#/components/headers/X-Rate-Limit-Reset'
            'X-Rate-Limit-Remaining':
              $ref: '#/components/headers/X-Rate-Limit-Remaining'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ClientErrorsResponse'
        '5XX':
          description: "Get seller failed due to internal errors. Please retry later.."
          headers:
            'X-Rate-Limit-Limit':
              $ref: '#/components/headers/X-Rate-Limit-Limit'
            'X-Rate-Limit-Reset':
              $ref: '#/components/headers/X-Rate-Limit-Reset'
            'X-Rate-Limit-Remaining':
              $ref: '#/components/headers/X-Rate-Limit-Remaining'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ServerErrorsResponse'

  /v4/marketplace/sellers/{id}:
    parameters:
      - $ref: '#/components/parameters/X-Header-Signature'
      - $ref: '#/components/parameters/X-Header-Merchant'
      - $ref: '#/components/parameters/X-Header-Date'
    put:
      tags:
       - Marketplace API
      summary: "Update seller"
      description: "Update the details of a marketplace seller with the given ID"
      parameters:
        - $ref: '#/components/parameters/X-Header-Idempotency-Key'
        - name: id
          in: path
          description: ID of the seller to update
          required: true
          schema:
            type: string
            format: uuid
            example: b4de-4c31-ac82-ac1ae54c-7cff8d290e58
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/MarketplaceSellerRequest'
      responses:
        '200':
          description: "Successfully updated a new marketplace seller."
          headers:
            'X-Rate-Limit-Limit':
              $ref: '#/components/headers/X-Rate-Limit-Limit'
            'X-Rate-Limit-Reset':
              $ref: '#/components/headers/X-Rate-Limit-Reset'
            'X-Rate-Limit-Remaining':
              $ref: '#/components/headers/X-Rate-Limit-Remaining'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MarketplaceSellerResponse'

        '4XX':
          description: "Update seller failed due to some invalid parameters."
          headers:
            'X-Rate-Limit-Limit':
              $ref: '#/components/headers/X-Rate-Limit-Limit'
            'X-Rate-Limit-Reset':
              $ref: '#/components/headers/X-Rate-Limit-Reset'
            'X-Rate-Limit-Remaining':
              $ref: '#/components/headers/X-Rate-Limit-Remaining'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ClientErrorsResponse'
        '5XX':
          description: "Update seller failed due to some internal errors. Please retry later.."
          headers:
            'X-Rate-Limit-Limit':
              $ref: '#/components/headers/X-Rate-Limit-Limit'
            'X-Rate-Limit-Reset':
              $ref: '#/components/headers/X-Rate-Limit-Reset'
            'X-Rate-Limit-Remaining':
              $ref: '#/components/headers/X-Rate-Limit-Remaining'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ServerErrorsResponse'

    get:
      tags:
       - Marketplace API
      summary: "Get seller"
      description: "Get details of a marketplace seller with the given ID"
      parameters:
        - name: id
          in: path
          description: ID of the seller to get
          required: true
          schema:
            type: string
            format: uuid
            example: b4de-4c31-ac82-ac1ae54c-7cff8d290e58
      responses:
        '200':
          description: "Successfully retrieved a marketplace seller."
          headers:
            'X-Rate-Limit-Limit':
              $ref: '#/components/headers/X-Rate-Limit-Limit'
            'X-Rate-Limit-Reset':
              $ref: '#/components/headers/X-Rate-Limit-Reset'
            'X-Rate-Limit-Remaining':
              $ref: '#/components/headers/X-Rate-Limit-Remaining'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MarketplaceSellerResponse'

        '4XX':
          description: "Get seller failed due to some invalid parameters."
          headers:
            'X-Rate-Limit-Limit':
              $ref: '#/components/headers/X-Rate-Limit-Limit'
            'X-Rate-Limit-Reset':
              $ref: '#/components/headers/X-Rate-Limit-Reset'
            'X-Rate-Limit-Remaining':
              $ref: '#/components/headers/X-Rate-Limit-Remaining'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ClientErrorsResponse'
        '5XX':
          description: "Get seller failed due to some internal errors. Please retry later.."
          headers:
            'X-Rate-Limit-Limit':
              $ref: '#/components/headers/X-Rate-Limit-Limit'
            'X-Rate-Limit-Reset':
              $ref: '#/components/headers/X-Rate-Limit-Reset'
            'X-Rate-Limit-Remaining':
              $ref: '#/components/headers/X-Rate-Limit-Remaining'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ServerErrorsResponse'

  /v4/marketplace/sellers/transfers:
    parameters:
    - $ref: '#/components/parameters/X-Header-Signature'
    - $ref: '#/components/parameters/X-Header-Merchant'
    - $ref: '#/components/parameters/X-Header-Date'
    - $ref: '#/components/parameters/X-Header-Idempotency-Key'
    post:
      tags:
        - Marketplace API
      summary: "Sellers Transfer"
      description: "Transfer money between sellers"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/MarketplaceSellerTransferRequest'
      responses:
        '200':
          description: "Successfully transfer between sellers."
          headers:
            'X-Rate-Limit-Limit':
              $ref: '#/components/headers/X-Rate-Limit-Limit'
            'X-Rate-Limit-Reset':
              $ref: '#/components/headers/X-Rate-Limit-Reset'
            'X-Rate-Limit-Remaining':
              $ref: '#/components/headers/X-Rate-Limit-Remaining'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MarketplaceSellerTransferResponse'
        '4XX':
          description: "Transfer failed due to invalid parameters."
          headers:
            'X-Rate-Limit-Limit':
              $ref: '#/components/headers/X-Rate-Limit-Limit'
            'X-Rate-Limit-Reset':
              $ref: '#/components/headers/X-Rate-Limit-Reset'
            'X-Rate-Limit-Remaining':
              $ref: '#/components/headers/X-Rate-Limit-Remaining'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ClientErrorsResponse'
        '5XX':
          description: "Transfer failed due to some internal errors. Please retry later.."
          headers:
            'X-Rate-Limit-Limit':
              $ref: '#/components/headers/X-Rate-Limit-Limit'
            'X-Rate-Limit-Reset':
              $ref: '#/components/headers/X-Rate-Limit-Reset'
            'X-Rate-Limit-Remaining':
              $ref: '#/components/headers/X-Rate-Limit-Remaining'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ServerErrorsResponse'

  /v4/marketplace/sellers/balance/debit:
    parameters:
    - $ref: '#/components/parameters/X-Header-Signature'
    - $ref: '#/components/parameters/X-Header-Merchant'
    - $ref: '#/components/parameters/X-Header-Date'
    - $ref: '#/components/parameters/X-Header-Idempotency-Key'
    post:
      tags:
        - Marketplace API
      summary: "Seller debit"
      description: "Debit money from the balance of the seller"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/MarketplaceSellerDebitRequest'
      responses:
        '200':
          description: "Successfully debited money from the balance of the seller."
          headers:
            'X-Rate-Limit-Limit':
              $ref: '#/components/headers/X-Rate-Limit-Limit'
            'X-Rate-Limit-Reset':
              $ref: '#/components/headers/X-Rate-Limit-Reset'
            'X-Rate-Limit-Remaining':
              $ref: '#/components/headers/X-Rate-Limit-Remaining'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MarketplaceSellerDebitResponse'
        '4XX':
          description: "Transfer failed due to invalid parameters."
          headers:
            'X-Rate-Limit-Limit':
              $ref: '#/components/headers/X-Rate-Limit-Limit'
            'X-Rate-Limit-Reset':
              $ref: '#/components/headers/X-Rate-Limit-Reset'
            'X-Rate-Limit-Remaining':
              $ref: '#/components/headers/X-Rate-Limit-Remaining'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ClientErrorsResponse'
        '5XX':
          description: "Transfer failed due to some internal errors. Please retry later.."
          headers:
            'X-Rate-Limit-Limit':
              $ref: '#/components/headers/X-Rate-Limit-Limit'
            'X-Rate-Limit-Reset':
              $ref: '#/components/headers/X-Rate-Limit-Reset'
            'X-Rate-Limit-Remaining':
              $ref: '#/components/headers/X-Rate-Limit-Remaining'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ServerErrorsResponse'

  /v4/marketplace/sellers/balance/credit:
    parameters:
    - $ref: '#/components/parameters/X-Header-Signature'
    - $ref: '#/components/parameters/X-Header-Merchant'
    - $ref: '#/components/parameters/X-Header-Date'
    - $ref: '#/components/parameters/X-Header-Idempotency-Key'
    post:
      tags:
        - Marketplace API
      summary: "Seller credit"
      description: "Credit money to the balance of the seller"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/MarketplaceSellerCreditRequest'
      responses:
        '200':
          description: "Successfully credited the balance of the seller."
          headers:
            'X-Rate-Limit-Limit':
              $ref: '#/components/headers/X-Rate-Limit-Limit'
            'X-Rate-Limit-Reset':
              $ref: '#/components/headers/X-Rate-Limit-Reset'
            'X-Rate-Limit-Remaining':
              $ref: '#/components/headers/X-Rate-Limit-Remaining'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MarketplaceSellerCreditResponse'
        '4XX':
          description: "Transfer failed due to invalid parameters."
          headers:
            'X-Rate-Limit-Limit':
              $ref: '#/components/headers/X-Rate-Limit-Limit'
            'X-Rate-Limit-Reset':
              $ref: '#/components/headers/X-Rate-Limit-Reset'
            'X-Rate-Limit-Remaining':
              $ref: '#/components/headers/X-Rate-Limit-Remaining'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ClientErrorsResponse'
        '5XX':
          description: "Transfer failed due to some internal errors. Please retry later.."
          headers:
            'X-Rate-Limit-Limit':
              $ref: '#/components/headers/X-Rate-Limit-Limit'
            'X-Rate-Limit-Reset':
              $ref: '#/components/headers/X-Rate-Limit-Reset'
            'X-Rate-Limit-Remaining':
              $ref: '#/components/headers/X-Rate-Limit-Remaining'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ServerErrorsResponse'

  /v4/marketplace/payoutRules:
    parameters:
      - $ref: '#/components/parameters/X-Header-Signature'
      - $ref: '#/components/parameters/X-Header-Merchant'
      - $ref: '#/components/parameters/X-Header-Date'
      - $ref: '#/components/parameters/X-Header-Idempotency-Key'
    get:
      tags:
        - Marketplace API
      summary: 'Payout rules'
      description: 'Get all existing payout rules'
      responses:
        '200':
          description: "Payout rules success response"
          headers:
            'X-Header-Signature':
              $ref: '#/components/headers/X-Header-Signature'
            'X-Header-Merchant':
              $ref: '#/components/headers/X-Header-Merchant'
            'X-Header-Date':
              $ref: '#/components/headers/X-Header-Date'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MarketplacePayoutRulesResponse'
        '5XX':
          $ref: '#/components/responses/5xxResponse'
  /v4/cardinfo/bin/{cardBin}:
    parameters:
      - $ref: '#/components/parameters/X-Header-Signature'
      - $ref: '#/components/parameters/X-Header-Merchant'
      - $ref: '#/components/parameters/X-Header-Date'
    get:
      tags:
        - CardInfo API
      summary: 'Get card information by bin'
      description: 'Get card information by card bin '
      parameters:
        - name: cardBin
          description: The card bin
          required: true
          in: path
          schema:
            example: 411111
            type: string
            minLength: 6
      responses:
        '200':
          description: "Card info success response"
          headers:
            'X-Header-Signature':
              $ref: '#/components/headers/X-Header-Signature'
            'X-Header-Merchant':
              $ref: '#/components/headers/X-Header-Merchant'
            'X-Header-Date':
              $ref: '#/components/headers/X-Header-Date'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CardInfoSuccessResponse'
        '4XX':
          $ref: '#/components/responses/4xxResponse'
        '5XX':
          $ref: '#/components/responses/5xxResponse'
        '429':
          $ref: '#/components/responses/TooManyRequestResponse'

  /v4/cardinfo/token/{token}:
    parameters:
      - $ref: '#/components/parameters/X-Header-Signature'
      - $ref: '#/components/parameters/X-Header-Merchant'
      - $ref: '#/components/parameters/X-Header-Date'
    get:
      tags:
        - CardInfo API
      summary: 'Get card information by token'
      description: 'Get card information by card token '
      parameters:
        - name: token
          description: The card token
          required: true
          in: path
          schema:
            example: d41d8cd98f00b204e9800998ecf8427e
            type: string
      responses:
        '200':
          description: "Card info success response"
          headers:
            'X-Header-Signature':
              $ref: '#/components/headers/X-Header-Signature'
            'X-Header-Merchant':
              $ref: '#/components/headers/X-Header-Merchant'
            'X-Header-Date':
              $ref: '#/components/headers/X-Header-Date'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CardInfoSuccessResponse'
        '4XX':
          $ref: '#/components/responses/4xxResponse'
        '5XX':
          $ref: '#/components/responses/5xxResponse'
        '429':
          $ref: '#/components/responses/TooManyRequestResponse'

  /v4/token:
    parameters:
      - $ref: '#/components/parameters/X-Header-Signature'
      - $ref: '#/components/parameters/X-Header-Merchant'
      - $ref: '#/components/parameters/X-Header-Date'
    post:
      tags:
        - Token API
      summary: 'Create token'
      description: |
        Creates a token associated with a card a buyer previously used for a payment.
        
        Depending on your account setup, when the token is created, a network token might associate with it as well. This is a virtual card issued by the card scheme (VISA, Mastercard) and it is the actual payment instrument used when processing the subsequent payments made by using the token. The network token itself is also visible in the banking platforms of the issuing bank, so the buyer has a better overview of where their card is saved. 
        
        Some information related to the token can be updated over time. Please see the [Get token info](#operation/Token-API-get-token-info) endpoint below.
        
        Note: not all previous payments can be used for tokenizing a buyer's card, and it depends on your account setup and certain other conditions (e.g. cards saved and used with the Apple Pay and Google Pay wallets can't be used to create a token).
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                payuPaymentReference:
                  $ref: '#/components/schemas/PayuPaymentReference'
              required:
                - payuPaymentReference
      responses:
        '200':
          description: "Token create success response"
          headers:
            'X-Header-Signature':
              $ref: '#/components/headers/X-Header-Signature'
            'X-Header-Merchant':
              $ref: '#/components/headers/X-Header-Merchant'
            'X-Header-Date':
              $ref: '#/components/headers/X-Header-Date'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TokenSuccessResponse'
        '4XX':
          $ref: '#/components/responses/4xxResponse'
        '5XX':
          $ref: '#/components/responses/5xxResponse'
        '429':
          $ref: '#/components/responses/TooManyRequestResponse'

  /v4/token/{token}:
    parameters:
      - $ref: '#/components/parameters/X-Header-Signature'
      - $ref: '#/components/parameters/X-Header-Merchant'
      - $ref: '#/components/parameters/X-Header-Date'
    get:
      tags:
        - Token API
      summary: 'Get token info'
      operationId: Token-API-get-token-info
      description: |
        Queries the system about the details of a token, by using the token provided by the previous endpoint.
        
        Based on your account setup, each token might generate and get linked to a network token, and because of this, the card number and expiration date (month and year) used for the subsequent payments will be usually different than the buyer's card.   

        In such cases, because the network token can be updated multiple times during the lifetime of a token, you should schedule the call of this endpoint to update the details of a token on your side from time to time.
        
        For instance, the expiration date of a token (last day on which the token can be used to create subsequent payments) is provided in the response in the `expirationDate` node. If this date is already in the past, then you won't be able to use the token anymore.
        
        Additionally, for UI purposes, if the buyer's card gets replaced and the network token is still available, then you should update the values returned by `lastFourDigits` and `cardExpirationDate`, as they will contain the values of the buyer's new issued card.
      parameters:
        - name: token
          description: The token
          required: true
          in: path
          schema:
            example: d41d8cd98f00b204e9800998ecf8427e
            type: string
      responses:
        '200':
          description: "Token info success response"
          headers:
            'X-Header-Signature':
              $ref: '#/components/headers/X-Header-Signature'
            'X-Header-Merchant':
              $ref: '#/components/headers/X-Header-Merchant'
            'X-Header-Date':
              $ref: '#/components/headers/X-Header-Date'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/GetTokenSuccessResponse'
        '4XX':
          $ref: '#/components/responses/4xxResponse'
        '5XX':
          $ref: '#/components/responses/5xxResponse'
        '429':
          $ref: '#/components/responses/TooManyRequestResponse'
    delete:
      tags:
        - Token API
      summary: 'Cancel token'
      description: 'Cancel a token'
      parameters:
        - name: token
          description: The card token info
          required: true
          in: path
          schema:
            example: d41d8cd98f00b204e9800998ecf8427e
            type: string
      responses:
        '200':
          description: "Cancel token success response"
          headers:
            'X-Header-Signature':
              $ref: '#/components/headers/X-Header-Signature'
            'X-Header-Merchant':
              $ref: '#/components/headers/X-Header-Merchant'
            'X-Header-Date':
              $ref: '#/components/headers/X-Header-Date'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TokenSuccessResponse'
        '4XX':
          $ref: '#/components/responses/4xxResponse'
        '5XX':
          $ref: '#/components/responses/5xxResponse'
        '429':
          $ref: '#/components/responses/TooManyRequestResponse'

  /merchant-notification-url:
    parameters:
      - $ref: '#/components/parameters/X-Header-Signature'
      - $ref: '#/components/parameters/X-Header-Merchant'
      - $ref: '#/components/parameters/X-Header-Date'
    post:
      tags:
        - Marketplace API
      summary: "Seller change webhook"
      description: "When a new seller is created or there is a change on an existing seller, the master account will be notified and the updated seller data will be sent as json to the notification url of the master account"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/MarketplaceSellerResponseNotification'
      responses:
        '200':
          description: Merchant should respond with this in order to indicate the notification was received succesfully. <br/>If the request fails (server does not respond properly, with the `200` HTTP code), it will be retried for a maximum of 5 attempts in a maximum period of 10 days.<br/>The time between each attempt will increase as the number of attempts increases, to avoid unnecessary requests when the IPN URL would be generally unavailable.
  /merchant-ipn-url:
    servers:
      - url: '/'
    parameters:
      - $ref: '#/components/parameters/X-Header-Signature'
      - $ref: '#/components/parameters/X-Header-Merchant'
      - $ref: '#/components/parameters/X-Header-Date'
    post:
      summary: 'PayU IPN Request'
      tags:
        - Webhooks
      description: This is the general structure of requests that PayU will sent to the merchant based on several payment flow events. The behavior of this can be changed from CPanel. <br/>
        <br/>
        For IPNs sent in case of refund orders information about products (like `name`, `sku`, `additionalDetails`) may be missing or different than the ones sent in Authorization request. <br/>
          In case of IPN for Refund orders, the product information will be sent only if it is a <b>"Full refund"</b> or a <b>"Partial refund that only has one product"</b>. Because of this you should not use these fields to match products or do specific logic based on it.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/IpnRequest'
      responses:
        '200':
          description: Merchant should respond with this in order to indicate the IPN was received successfully. If the request fails (server does not respond properly, with the `200` HTTP code), it will be retried for a maximum of 50 attempts in a maximum period of 10 days. The time between each attempt will increase as the number of attempts increases, to avoid unnecessary requests when the IPN URL would be generally unavailable.

  /merchant-token-notifications:
    parameters:
      - $ref: '#/components/parameters/X-Header-Merchant'
      - $ref: '#/components/parameters/X-Header-Date'
      - $ref: '#/components/parameters/X-Header-Signature'
      - $ref: '#/components/parameters/X-Header-Event-Type'
    post:
      summary: 'Merchant Token Notifications'
      tags:
        - Webhooks
      description: The Merchant Token Notifications feature is designed to provide merchants with real-time notifications on any updates that occurred on the merchant token.
        When a notification is received, a <a href="/docs/#operation/Token-API-get-token-info">GET Token Info</a> request will be required to get the updated token information.
        Keep in mind that a <code>delete</code> event signals a final status change.
        <br/>
        This feature can be enabled and configured via CPanel, from Account Management > Account settings > Merchant Token Notifications.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/MerchantTokenNotification'
      responses:
        '200':
          description: Merchant should respond with this HTTP code in order to indicate the notification was received successfully. 
            If the request fails (server does not respond properly, with the `200` HTTP code), it will be retried for a maximum of 50 attempts in a maximum period of 10 days.
            The time between each attempt will increase as the number of attempts increases, to avoid unnecessary requests when the Webhook URL would be generally unavailable.

  /v4/fx/rates/{baseCurrency}:
    parameters:
      - $ref: '#/components/parameters/X-Header-Signature'
      - $ref: '#/components/parameters/X-Header-Merchant'
      - $ref: '#/components/parameters/X-Header-Date'
    get:
      tags:
        - FX API
      summary: 'Get all FX exchange rates'
      description: 'Retrieves all the rates reported to the baseCurrency currency. The FX rates are available until the expiration date (therefore we recommend you to store or cache the API result). If you receive an error on the authorization step when making your payment, concerning that FX rates are invalid, you should retrieve these again.'
      parameters:
        - name: baseCurrency
          description: Currency used for exchanging to other currencies
          required: true
          in: path
          schema:
            example: RON
            type: string
      responses:
        '200':
          description: "FX exchange rates success response"
          headers:
            'X-Header-Signature':
              $ref: '#/components/headers/X-Header-Signature'
            'X-Header-Merchant':
              $ref: '#/components/headers/X-Header-Merchant'
            'X-Header-Date':
              $ref: '#/components/headers/X-Header-Date'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/FXExchangeRates'
        '204':
          description: "There are no rates for the provided base currency."
          headers:
            'X-Header-Signature':
              $ref: '#/components/headers/X-Header-Signature'
            'X-Header-Merchant':
              $ref: '#/components/headers/X-Header-Merchant'
            'X-Header-Date':
              $ref: '#/components/headers/X-Header-Date'
        '4XX':
          $ref: '#/components/responses/4xxResponse'
        '5XX':
          $ref: '#/components/responses/5xxResponse'
        '429':
          $ref: '#/components/responses/TooManyRequestResponse'

  /v4/payments/sessions:
    parameters:
      - $ref: '#/components/parameters/X-Header-Signature'
      - $ref: '#/components/parameters/X-Header-Merchant'
      - $ref: '#/components/parameters/X-Header-Date'
      - $ref: '#/components/parameters/X-Header-Idempotency-Key'
    post:
      tags:
        - Sessions
      summary: 'Create a session'
      description: Creates a session to be used when authorizing with oneTimeUseToken. A new session should be generated for every successful authorization with oneTimeUseToken.
      requestBody:
        required: false
        content:
          application/json:
            schema:
              type: object
              properties:
                lifetimeMinutes:
                  description: The session lifetime in minutes. If it is not present, the default will be the platform value
                  format: number
                  example: 10
                  minimum: 1
                  maximum: 1440
      responses:
        '200':
          description: "Sessions create success response"
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SessionsSuccessResponse'
        '400':
          description: "Sessions client error response"
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SessionsClientErrorResponse'
        '500':
          description: "Sessions server error response"
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SessionsServerErrorResponse'

components:
  parameters:
    merchantPaymentReference:
      name: merchantPaymentReference
      in: path
      description: The Merchant payment reference
      required: true
      schema:
        anyOf:
          - type: string
          - type: number

    X-Header-Signature:
      name: X-Header-Signature
      in: header
      description: 'Signature of the message'
      required: true
      example: 0b9b07bd4b81375d189bbe0fe23a7c4b939b112715c2ac090829ed2182752c1c
      schema:
        type: string

    X-Header-Merchant:
      name: X-Header-Merchant
      in: header
      description: "Merchant identifier in PayU system"
      required: true
      example:
        - MERCH_V2
        - GLB_MKPT
      schema:
        type: string

    X-Header-Submerchant-Id:
      name: X-Header-Submerchant-Id
      in: header
      description: "Identifier of the submerchant for which this request will be done. The one doing the call needs to be a Payment Facilitator"
      required: false
      example:
        - SUB_1
        - SUB_2
      schema:
        type: string
        maxLength: 50

    X-Header-Date:
      name: X-Header-Date
      in: header
      description: 'Date of the request in ISO_8601 format, with timezone designator (https://en.wikipedia.org/wiki/ISO_8601).'
      required: true
      schema:
        format: ISO_8601
      example: '2011-12-03T10:15:30+01:00'

    X-Header-Idempotency-Key:
      name: X-Header-Idempotency-Key
      in: header
      description: 'An idempotency key is a unique value generated by the client which the server uses to recognize subsequent retries of the same request.'
      schema:
        type: string
      example: '60ibwxptqpsw7czp0u4zzwjj3fhmnfozmw08'

    X-Header-Event-Type:
      name: X-Header-Event-Type
      in: header
      description: 'The type of the event that triggered the notification.'
      required: true
      schema:
        type: string
        enum: ['create', 'update', 'delete']

  headers:
    X-Header-Signature:
      description: 'Signature of the message'
      required: true
      example: 0b9b07bd4b81375d189bbe0fe23a7c4b939b112715c2ac090829ed2182752c1c
      schema:
        type: string

    X-Header-Merchant:
      description: "Merchant identifier in PayU system"
      required: true
      example: MERCH_V2
      schema:
        type: string

    X-Header-Date:
      description: 'Date of the request in ISO_8601 format, with timezone designator (https://en.wikipedia.org/wiki/ISO_8601).'
      required: true
      schema:
        format: ISO_8601
      example: '2011-12-03T10:15:30+01:00'

    X-Rate-Limit-Limit:
      description: 'Number of allowed requests for a period of 60 seconds.'
      schema:
        type: number
        format: int32
      example: 122

    X-Rate-Limit-Reset:
      description: 'How much time remains, in seconds, until the end of the current period of 60 seconds.'
      schema:
        type: number
        format: int32
      example: 122

    X-Rate-Limit-Remaining:
      description: 'Requests available until the end of current period of 60 seconds.'
      schema:
        type: number
        format: int32
      example: 0

  securitySchemes:
    Merchant:
      type: apiKey
      description: Your code identifier in our system (you can find it in CPanel > Account Management > Account Settings > "Vendor code" field)
      in: header
      name: X-Header-Merchant
    Date:
      type: apiKey
      description: Date of the request in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format (e.g. 2020-01-01T11:22:33+03:00)
      in: header
      name: X-Header-Date
    Signature:
      type: apiKey
      description: >
        Signature is obtained by applying the `HMAC-SHA256` algorithm (your secret key is the encryption key) to the following concatenated string:
         - `X-Header-Merchant` header value
         - `X-Header-Date` header value
         - HTTP method (`POST`, `GET`, `PUT`, `DELETE`)
         - base path from API call URL. (eg: `/api/v4/payments/authorize`)
         - query string from API call URL (if there is any)
         - computed MD5 (lowercase hexadecimal) of the request payload body

        All signature characters should be lowercase hexadecimal characters (i.e.: `da0b9f5e7e12cd02f02ed1591802d3739762a69c0ea31e8a3b28e6eb817b73ec`).


        Your secret key can be found in the CPanel, under Account Management / Account Settings section. If you require additional assistance for this step, please contact us.


        The base path and query string is computed as specified by [RFC3986](https://www.ietf.org/rfc/rfc3986.txt)'s "Syntax Components" section.


        If your request has no payload body, then the last item from the above list will be the computed MD5 of the empty string "". An example here would be any `GET` request.
      in: header
      name: X-Header-Signature

  schemas:
    BalanceClientErrorResponse:
      properties:
        code:
          $ref: '#/components/schemas/400ResponseCode'
        message:
          $ref: '#/components/schemas/BalanceClientErrorMessage'
        status:
          $ref: '#/components/schemas/PayoutClientErrorStatus'

    PayoutHistoryClientErrorResponse:
      properties:
        code:
          $ref: '#/components/schemas/400ResponseCode'
        message:
          $ref: '#/components/schemas/PayoutHistoryClientErrorMessage'
        status:
          $ref: '#/components/schemas/PayoutClientErrorStatus'

    PayoutBalanceSuccessResponse:
      type: object
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/PayoutBalanceItem'
        code:
          $ref: '#/components/schemas/2xxResponseCode'
        message:
          $ref: '#/components/schemas/ResponseMessage'
        status:
          $ref: '#/components/schemas/SuccessResponseStatus'

    PayoutBalanceItem:
      type: object
      properties:
        merchantCode:
          $ref: '#/components/schemas/MerchantCode'
        currency:
          $ref: '#/components/schemas/Currency'
        value:
          $ref: '#/components/schemas/BalanceAmount'
        timestamp:
          $ref: '#/components/schemas/BalanceTimestamp'
      required:
        - merchantCode
        - currency
        - value
        - timestamp

    SuccessResponseStatus:
      type: string
      example: "A text representing the status of the response"
      enum:
        - SUCCESS

    BalanceTimestamp:
      type: string
      description: Date time when balance was calculated. Must be in ISO_8601 format (https://en.wikipedia.org/wiki/ISO_8601)
      format: ISO_8601 date-time
      example: 2021-06-01 10:20:01
      minLength: 1

    PayoutHistoryStartDate:
      type: string
      description: 'Date start of search payouts in ISO_8601 Y-m-d\TH:i:sP format (https://en.wikipedia.org/wiki/ISO_8601)'
      format: ISO_8601
      example: '2021-04-12T16:40:00-04:00'

    PayoutHistoryEndDate:
      type: string
      description: 'Date end of search payouts in ISO_8601 Y-m-d\TH:i:sP format (https://en.wikipedia.org/wiki/ISO_8601)'
      format: ISO_8601
      example: '2021-04-12T16:40:00-04:00'

    PayoutHistorySuccessResponse:
      type: object
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/PayoutResponseObject'
        _links:
          description: Page navigation links used to retrieve all the payouts requested initially, as each API request is limited to maximum 50 items. The url from "next" node should be called as long as it exists. When it no longer comes in the response, it means that you are on the last page and all the payouts were retrieved.
          type: object
          properties:
            prev:
              $ref: '#/components/schemas/PaginationPrev'
            next:
              $ref: '#/components/schemas/PaginationNext'
            last:
              $ref: '#/components/schemas/PaginationLast'
        code:
          $ref: '#/components/schemas/2xxResponseCode'
        message:
          $ref: '#/components/schemas/ResponseMessage'
        status:
          $ref: '#/components/schemas/SuccessResponseStatus'
      required:
        - items
        - _links
        - code
        - message
        - status

    MerchantCode:
      type: string
      description: Merchant identifier in PayU system
      example: MERCH_V1
      minLength: 1

    PayoutUnauthorizedResponse:
      type: object
      properties:
        code:
          $ref: '#/components/schemas/401ResponseCode'
        message:
          $ref: '#/components/schemas/ErrorMessage'
        status:
          $ref: '#/components/schemas/UnauthorizedRequestStatus'

    MarketplaceVersion:
      type: number
      format: double
      example: 2.0
      default: 2.0
      description: "Version of Marketplace package activated. If it's not specified it will be considered as version 2. If it is specified, it should be the same for all products"

    UnauthorizedRequestStatus:
      type: string
      example: INVALID_CREDENTIALS
      enum:
        - INVALID_CREDENTIALS

    401ResponseCode:
      type: number
      enum: [401]
      example: 401
      description: "A bad request code (http code that is also returned in headers)"

    PayoutTooManyRequestResponse:
      type: object
      properties:
        code:
          $ref: '#/components/schemas/429ResponseCode'
        message:
          $ref: '#/components/schemas/ErrorMessage'
        status:
          $ref: '#/components/schemas/LimitRequestStatus'

    429ResponseCode:
      type: number
      enum: [ 429 ]
      example: 429
      description: "A bad request code (http code that is also returned in headers)"

    LimitRequestStatus:
      type: string
      example: LIMIT_CALLS_EXCEEDED
      enum:
        - LIMIT_CALLS_EXCEEDED

    PayoutServerErrorsResponse:
      type: object
      properties:
        code:
          $ref: '#/components/schemas/500ResponseCode'
        message:
          $ref: '#/components/schemas/InternalErrorMessage'
        status:
          $ref: '#/components/schemas/InternalErrorStatus'

    BadGatewayResponse:
      type: object
      properties:
        code:
          $ref: '#/components/schemas/502ResponseCode'
        message:
          $ref: '#/components/schemas/ErrorMessage'

    500ResponseCode:
      type: number
      enum: [ 500 ]
      example: 500
      description: "Some error occurred trying to process request (http code that is also returned in headers)"

    502ResponseCode:
      type: number
      enum: [ 502 ]
      example: 502
      description: "Bad Gateway Response Code"

    PayoutClientErrorResponse:
      type: object
      properties:
        code:
          $ref: '#/components/schemas/400ResponseCode'
        message:
          $ref: '#/components/schemas/PayoutClientErrorMessage'
        status:
          $ref: '#/components/schemas/PayoutClientErrorStatus'

    400ResponseCode:
      type: number
      enum: [ 400 ]
      example: 400
      description: "A bad request code (http code that is also returned in headers)"

    BalanceClientErrorMessage:
      description: Reason why request failed.
      enum:
        - 'Invalid merchant codes'
        - 'Invalid min value'
        - 'Invalid max value'
        - 'Max value should be greater than the min value'
        - 'Invalid currency'
        - 'Invalid merchant'
      type: string
      example: "A text message with details about processing result or with some message error"

    PayoutHistoryClientErrorMessage:
      description: Reason why request failed.
      enum:
        - 'Invalid start date'
        - 'Invalid end date'
        - 'Start date can not be greater than current date'
        - 'Start date can not be greater than end date'
        - 'Invalid merchant codes'
        - 'Invalid page'
        - 'Invalid merchant'
      type: string
      example: "A text message with details about processing result or with some message error"

    PayoutClientErrorStatus:
      enum:
        - INVALID_REQUEST_STRUCTURE
        - INVALID_REQUEST
      type: string
      example: "A text representing the status of the response"

    PayoutClientErrorMessage:
      description: Reason why request failed.
      enum:
        - 'Invalid merchant'
        - 'The merchant does not have the needed setup'
        - 'Invalid amount'
        - 'Not enough balance'
        - 'Invalid card number'
        - 'Invalid merchantPayoutReference'
        - 'Invalid currency'
        - 'Invalid content type'
        - 'No parameters specified!'
        - 'No amount specified'
        - 'Invalid amount specified'
        - 'No amount currency specified'
        - 'No amount value specified'
        - 'No merchant reference specified'
        - 'No description specified'
        - 'No destination specified'
        - 'Invalid destination'
        - 'No destination type specified'
        - 'No destination card specified'
        - 'Invalid destination card'
        - 'No destination cardNumber specified'
        - 'No token specified'
        - 'Invalid destination type'
        - 'No destination recipient specified'
        - 'Invalid destination recipient'
        - 'No destination recipient type specified'
        - 'No destination recipient email specified'
        - 'No destination recipient city specified'
        - 'No destination recipient address specified'
        - 'No destination recipient postalCode specified'
        - 'No destination recipient countryCode specified'
        - 'No destination recipient first and last name specified'
        - 'Invalid destination recipient specified: name is not allowed'
        - 'No destination recipient name specified'
        - 'Invalid destination recipient specified: first or last name is not allowed'
        - 'Invalid destination recipient type'
        - 'No source specified'
        - 'Invalid source'
        - 'No source type specified'
        - 'Invalid source type'
      type: string
      example: "A text message with details about processing result or with some message error"

    PayoutResponseStatus:
        type: string
        description: A text representing the status of the response
        enum:
          - SUCCESS
          - GW_PENDING
          - GW_ERROR

    PayoutSuccessResponse:
      allOf:
        - $ref: '#/components/schemas/PayoutResponseObject'
        - type: object
          properties:
            code:
              $ref: '#/components/schemas/2xxResponseCode'
            message:
              $ref: '#/components/schemas/ResponseMessage'
            status:
              $ref: '#/components/schemas/PayoutResponseStatus'
          required:
            - code
            - message
            - status

    PayoutResponseObject:
      type: object
      properties:
        payuPayoutReference:
          $ref: '#/components/schemas/PayuPayoutReference'
        payoutStatus:
          $ref: '#/components/schemas/PayoutStatus'
        amount:
          $ref: '#/components/schemas/PayoutAmount'
        merchantCode:
          $ref: '#/components/schemas/MerchantCode'
        commission:
          $ref: '#/components/schemas/PayoutCommission'
        merchantPayoutReference:
          $ref: '#/components/schemas/MerchantPayoutReference'
        description:
          $ref: '#/components/schemas/PayoutDescription'
        destination:
          $ref: '#/components/schemas/PayoutDestinationResponse'
        source:
          $ref: '#/components/schemas/PayoutSource'
      required:
        - payuPayoutReference
        - payoutStatus
        - merchantPayoutReference
        - amount
        - merchantCode
        - commission
        - description
        - destination
        - source

    PayoutStatus:
      type: string
      enum: [ 'SUCCESS', 'PENDING', 'FAILED' ]
      description: 'Payout operation status'

    PayuPayoutReference:
      description: This is our internal payout identifier
      type: string
      example: "123"

    MerchantCreateRequest:
      type: object
      required:
        - name
        - companyName
        - externalId
        - contact
        - taxId
        - registrationNumber
        - mccCode
        - websiteUrl
      properties:
        name:
          type: string
          description: "Commercial name of the company"
          example: "testAcc12"
        companyName:
          type: string
          description: "Legal name of the company"
          example: "SC Test Software SRL"
        externalId:
          type: string
          description: "External identifier"
        contact:
          $ref: '#/components/schemas/MerchantContact'
        taxId:
          type: string
          description: "Tax identificator"
          example: "RO3847538"
        registrationNumber:
          type: string
          description: "Registration number"
          example: "J2023021741111"
        mccCode:
          type: string
          description: "Category code"
          example: "0742"
        websiteUrl:
          type: string
          format: uri
          example: "http://www.test.com"

    MerchantContact:
      type: object
      required:
        - legalRepresentative
        - address
        - email
        - phone
      properties:
        legalRepresentative:
          type: string
          description: "Name of the legal representative"
        address:
          $ref: '#/components/schemas/MerchantAddress'
        email:
          type: string
          format: email
          example: "test@acc.com"
        phone:
          type: string
          format: phone
          example: "7643829857"

    MerchantAddress:
      type: object
      properties:
        street:
          type: string
          example: "Florilor 4"
        city:
          type: string
          example: "Bucuresti"
        postalCode:
          type: string
          example: "123456"
        country:
          type: string
          example: "RO"

    MerchantCreateResponse:
      type: object
      required:
        - code
        - name
        - companyName
        - externalId
        - contact
        - taxId
        - registrationNumber
        - mccCode
        - websiteUrl
      properties:
        code:
          type: string
          description: "Code of the newly created merchant"
          example: "CAHF83"
        name:
          type: string
          description: "Commercial name of the company"
          example: "testAcc12"
        companyName:
          type: string
          description: "Legal name of the company"
          example: "SC Test Software SRL"
        externalId:
          type: string
          description: "External identifier"
        contact:
          $ref: '#/components/schemas/MerchantContact'
        taxId:
          type: string
          description: "Tax identificator"
          example: "RO3847538"
        registrationNumber:
          type: string
          description: "Registration number"
          example: "J2023021741111"
        mccCode:
          type: string
          description: "Category code"
          example: "0742"
        websiteUrl:
          type: string
          format: uri
          example: "http://www.test.com"

    PayoutRequest:
      type: object
      properties:
        merchantPayoutReference:
          $ref: '#/components/schemas/MerchantPayoutReference'
        amount:
          $ref: '#/components/schemas/PayoutAmount'
        description:
          $ref: '#/components/schemas/PayoutDescription'
        destination:
          $ref: '#/components/schemas/PayoutDestination'
        source:
          $ref: '#/components/schemas/PayoutSource'
      required:
        - merchantPayoutReference
        - amount
        - description
        - destination
        - source

    PayoutSource:
      description: This is the source from which the payout amount will be retrieved. The only value supported for now for this field is "merchantBalance"
      type: object
      properties:
        type:
          type: string
          enum: [ 'merchantBalance' ]
          description: 'Payout Source'
          minLength: 1
        sender:
          $ref: '#/components/schemas/PayoutSourceSender'
      required:
        - type
        - sender


    PayoutSourceSender:
      description:  This is the sender details for the payout.
      type: object
      properties:
        firstName:
          type: string
          description: 'Sender First Name'
          example: John
          minLength: 1
        lastName:
          type: string
          description: 'Sender Last Name'
          example: John
          minLength: 1
        email:
          type: string
          description: 'Sender e-mail address'
          example: 'senderEmail@mail.com'
          minLength: 1
        phone:
          type: string
          description: 'Sender phone'
          example: '0764111111'
          minLength: 1
      required:
        - firstName
        - lastName
        - email
        - phone

    PayoutDestination:
      description: 'Object containing destination info'
      type: object
      discriminator:
        propertyName: type
        mapping:
          card: '#/components/schemas/CardDestination'
          token: '#/components/schemas/TokenDestination'
      anyOf:
        - $ref: '#/components/schemas/CardDestination'
        - $ref: '#/components/schemas/TokenDestination'

    PayoutDestinationResponse:
      description: 'Object containing destination info'
      type: object
      properties:
        type:
          type: string
          enum: [ 'card', 'token' ]
          description: 'Destination type'
          minLength: 1
        recipient:
          $ref: '#/components/schemas/PayoutRecipient'

    PayoutHistoryPagination:
      type: number
      format: int
      example: 2

    CardDestination:
      type: object
      properties:
        type:
          type: string
          enum: [ 'card', 'token' ]
          description: 'Destination type'
          minLength: 1
        card:
          $ref: '#/components/schemas/CardObject'
        recipient:
          $ref: '#/components/schemas/PayoutRecipient'
      required:
        - type
        - card
        - recipient

    TokenDestination:
      type: object
      properties:
        type:
          type: string
          enum: [ 'card', 'token' ]
          description: 'Destination type'
          minLength: 1
        token:
          $ref: '#/components/schemas/TokenObject'
        recipient:
          $ref: '#/components/schemas/PayoutRecipient'
      required:
        - type
        - token
        - recipient

    CardObject:
      type: object
      properties:
        cardNumber:
          anyOf:
            - type: string
            - type: number
          description: 'Card number'
          example: '4111111111111111'
      required:
        - cardNumber

    TokenObject:
      type: object
      properties:
        tokenHash:
          type: string
          description: 'Token'
          example: 'd41d8cd98f00b204e9800998ecf8427e'
          minLength: 1
      required:
        - tokenHash



    PayoutRecipient:
      description: 'Object containing recipient info'
      type: object
      discriminator:
        propertyName: type
        mapping:
          individual: '#/components/schemas/PayoutRecipientIndividual'
          business: '#/components/schemas/PayoutRecipientBusiness'
      anyOf:
        - $ref: '#/components/schemas/PayoutRecipientIndividual'
        - $ref: '#/components/schemas/PayoutRecipientBusiness'

    PayoutRecipientIndividual:
      type: object
      title: 'Individual Type'
      properties:
        type:
          type: string
          enum: [ 'individual', 'business' ]
          description: 'Recipient type'
          minLength: 1
        email:
          type: string
          example: 'example@email.com'
          description: Recipient's email
          minLength: 1
        city:
          description: Recipient's city
          type: string
          example: Bucharest
          minLength: 1
        address:
          description: Recipient's address
          type: string
          example: Sector 2
          minLength: 1
        postalCode:
          type: string
          example: "510002"
          description: Recipient's postal code
          minLength: 1
        countryCode:
          type: string
          example: RO
          description: Recipient's country code
          minLength: 1
        firstName:
          description: "Recipient's first name."
          type: string
          example: John
          minLength: 1
        lastName:
          description: "Recipient's last name."
          type: string
          example: Doe
          minLength: 1
      required:
        - type
        - email
        - city
        - address
        - postalCode
        - countryCode
        - firstName
        - lastName

    PayoutRecipientBusiness:
      type: object
      title: 'Business Type'
      properties:
        type:
          type: string
          enum: [ 'individual', 'business' ]
          description: 'Recipient type'
          minLength: 1
        email:
          type: string
          example: 'example@email.com'
          description: Recipient's email
          minLength: 1
        city:
          description: Recipient's city
          type: string
          example: Bucharest
          minLength: 1
        address:
          description: Recipient's address
          type: string
          example: Sector 2
          minLength: 1
        postalCode:
          type: string
          example: "510002"
          description: Recipient's postal code
          minLength: 1
        countryCode:
          type: string
          example: RO
          description: Recipient's country code
          minLength: 1
        name:
          description: "Recipient's name."
          type: string
          example: Doe
          minLength: 1
      required:
        - type
        - email
        - city
        - address
        - postalCode
        - countryCode
        - name

    PayoutDescription:
      description: "Details of payout"
      type: string
      maxLength: 255
      example: "Description of payout"

    PayoutAmount:
      description: Object containing information about the payout amount
      type: object
      properties:
        currency:
          $ref: '#/components/schemas/Currency'
        value:
          $ref: '#/components/schemas/PayoutAmountValue'
      required:
        - currency
        - value

    PayoutAmountValue:
      description: Amount that will be transferred
      anyOf:
        - type: string
        - type: number
          format: double
      example: 5.66
      minimum: 0
      exclusiveMinimum: true


    PayoutCommission:
      description: Object containing information about the payout commission
      type: object
      properties:
        merchant:
          $ref: '#/components/schemas/PayoutMerchantCommission'
        payee:
          $ref: '#/components/schemas/PayoutPayeeCommission'

    PayoutMerchantCommission:
      description: Merchant commission amount
      type: number
      format: double
      example: 5.66
      minimum: 0

    PayoutPayeeCommission:
      description: Payee commission amount
      type: number
      format: double
      example: 2.66
      minimum: 0

    BalanceMinAmount:
      type: number
      format: double
      example: 5.66
      minimum: 0
      exclusiveMinimum: true

    BalanceAmount:
      description: Balance amount
      type: number
      format: double
      example: 5.66
      minimum: 0
      exclusiveMinimum: true

    BalanceMaxAmount:
      type: number
      format: double
      example: 5.66
      minimum: 0
      exclusiveMinimum: true

    CardInfoSuccessResponse:
      allOf:
        - type: object
          properties:
            code:
              $ref: '#/components/schemas/2xxResponseCode'
            message:
              $ref: '#/components/schemas/ResponseMessage'
            status:
              $ref: '#/components/schemas/SuccessResponseStatus'
          required:
            - code
            - message
            - status
        - $ref: '#/components/schemas/CardInfoItem'

    CardInfoItem:
      type: object
      properties:
        binNumber:
          type: string
          example: 411111
          description: BIN(first 6 digits) of the requested card
        cardScheme:
          type: string
          example: VISA
          enum:
            - VISA
            - VISA ELECTRON
            - MASTERCARD
            - MAESTRO
            - DISCOVER
            - AMEX
            - TROY
            - MIR
            - UNIONPAY
            - OTHER
        issuerBank:
          type: string
          example: BRD Groupe Societe Generale
          description: Name of the bank that issued the card
        issuerCountryCode:
          type: string
          example: RO
          description: ISO 3166-1 alpha-2 country code where the card was issued
        cardType:
          type: string
          example: DEBIT
          enum:
            - DEBIT
            - CREDIT
            - PREPAID
            - UNKNOWN
        cardProfile:
          type: string
          enum:
            - CONSUMER
            - COMMERCIAL
            - UNKNOWN
            - BOTH
          example: CONSUMER
        cardProgram:
          type: string
          example: Name of the program
          description: Name of the program in which the card is enrolled. Comes empty if the card is not enrolled in any.
        cardProgramSettings:
          type: array
          description: The settings are used to determine the card's eligibility for certain features, such as installments.
          items:
            type: object
            properties:
              minimumOrderAmount:
                type: number
                example: 500
                description: Minimum order amount for which the card can be used with installments
        installmentOptions:
          type: array
          items:
            type: object
            properties:
              installmentNumber:
                type: number
                example: 1
                description: Number of installments for this installment plan
        paymentMethod:
          type: string
          example: CCVISAMC
          description: the payment method to be used for payments with this card
      required:
        - binNumber

    FXExchangeRates:
      allOf:
        - type: object
          properties:
            code:
              $ref: '#/components/schemas/2xxResponseCode'
            message:
              $ref: '#/components/schemas/ResponseMessage'
            status:
              $ref: '#/components/schemas/SuccessResponseStatus'
          required:
            - code
            - message
            - status
        - $ref: '#/components/schemas/FXExchangeRatesItem'

    FXExchangeRatesItem:
      type: object
      properties:
        baseCurrency:
          type: string
          example: "RON"
          description: Currency used for exchanging to other currencies
        rates:
          type: object
          description: |
            List of exchange rates for all available currencies for FX.\
            The precision of the exchange rate differs depending on the currencies' smallest unit (number of decimals).\
            It is calculated as the difference in number of decimals of the currencies plus 4, to ensure enough significant digits.\
            For example: RON to EUR will have 4 decimals precision, RON to HUF will have 2, while HUF to RON will have 6.
          properties:
            EUR:
              type: string
              example: '0.2132'
            IQD:
              type: string
              example: '279.068'
            HUF:
              type: string
              example: '77.41'
        expiresAt:
          description: Expiration of the FX rates
          type: string
          format: ISO_8601 datetime
          example: '2027-01-02T12:00:14+00:00'
      required:
        - baseCurrency
        - rates
        - expiresAt


    AuthorizeResponse:
      type: object
      required:
        - code
        - message
        - payuPaymentReference
        - amount
        - authorization
      properties:
        code:
          $ref: '#/components/schemas/2xxResponseCode'
        message:
          $ref: '#/components/schemas/ResponseMessage'
        payuPaymentReference:
          $ref: '#/components/schemas/PayuPaymentReference'
        merchantPaymentReference:
          $ref: '#/components/schemas/MerchantPaymentReference'
        amount:
          $ref: '#/components/schemas/PriceAmount'
        currency:
          $ref: '#/components/schemas/Currency'
        paymentResult:
          $ref: '#/components/schemas/PaymentResult'
        authorization:
          $ref: '#/components/schemas/AuthorizationResource'

    ConfirmSuccessResponse:
      type: object
      properties:
        payuPaymentReference:
          $ref: '#/components/schemas/PayuPaymentReference'
        code:
          $ref: '#/components/schemas/2xxResponseCode'
        message:
          $ref: '#/components/schemas/ResponseMessage'

    ConfirmSuccessStatusResponse:
      type: object
      properties:
        payuPaymentReference:
          $ref: '#/components/schemas/PayuPaymentReference'
        code:
          $ref: '#/components/schemas/2xxResponseCode'
        message:
          $ref: '#/components/schemas/ResponseMessage'
        status:
          $ref: '#/components/schemas/IdnResponseStatus'
    BasicClientErrorsResponse:
      type: object
      properties:
        code:
          $ref: '#/components/schemas/4xxResponseCode'
        message:
          $ref: '#/components/schemas/ClientErrorResponseMessage'

    ClientErrorsResponse:
      type: object
      properties:
        code:
          $ref: '#/components/schemas/4xxResponseCode'
        message:
          $ref: '#/components/schemas/ResponseMessage'
        payuPaymentReference:
          $ref: '#/components/schemas/PayuPaymentReference'
    AluClientErrorsResponse:
      type: object
      properties:
        code:
          $ref: '#/components/schemas/4xxResponseCode'
        message:
          $ref: '#/components/schemas/ResponseMessage'
        status:
          $ref: '#/components/schemas/ClientResponseStatus'

    IdnClientErrorsStatusResponse:
      type: object
      properties:
        code:
          $ref: '#/components/schemas/4xxResponseCode'
        message:
          $ref: '#/components/schemas/ResponseMessage'
        payuPaymentReference:
          $ref: '#/components/schemas/PayuPaymentReference'
        status:
          $ref: '#/components/schemas/IdnResponseStatus'

    IrnClientErrorsStatusResponse:
      type: object
      properties:
        code:
          $ref: '#/components/schemas/4xxResponseCode'
        message:
          $ref: '#/components/schemas/ResponseMessage'
        payuPaymentReference:
          $ref: '#/components/schemas/PayuPaymentReference'
        status:
          $ref: '#/components/schemas/IrnResponseStatus'

    IrnClientAlreadyAuthStatusResponse:
      type: object
      properties:
        code:
          type: number
          example: 202
        message:
          type: string
          example: "Order already cancelled"
        payuPaymentReference:
          $ref: '#/components/schemas/PayuPaymentReference'
        status:
          type: string
          example: "ALREADY_CANCELLED"

    ServerErrorsResponse:
      type: object
      properties:
        code:
          $ref: '#/components/schemas/5xxResponseCode'
        message:
          $ref: '#/components/schemas/ResponseMessage'

    IdnServerErrorsStatusResponse:
      type: object
      properties:
        code:
          $ref: '#/components/schemas/5xxResponseCode'
        message:
          $ref: '#/components/schemas/ResponseMessage'
        payuPaymentReference:
          $ref: '#/components/schemas/PayuPaymentReference'
        status:
          $ref: '#/components/schemas/IdnResponseStatus'

    IrnServerErrorsStatusResponse:
      type: object
      properties:
        code:
          $ref: '#/components/schemas/5xxResponseCode'
        message:
          $ref: '#/components/schemas/ResponseMessage'
        payuPaymentReference:
          $ref: '#/components/schemas/PayuPaymentReference'
        status:
          $ref: '#/components/schemas/IrnResponseStatus'

    NotFoundResponse:
      type: object
      properties:
        code:
          $ref: '#/components/schemas/404ResponseCode'
        message:
          $ref: '#/components/schemas/NotFoundMessage'

    RefundSuccessStatusResponse:
      type: object
      properties:
        payuPaymentReference:
          $ref: '#/components/schemas/PayuPaymentReference'
        code:
          type: number
          enum: [200]
        message:
          type: string
          enum: ["Confirmed", "Order already confirmed", "OK"]
        status:
          $ref: '#/components/schemas/IrnResponseStatus'
        refundRequestId:
          $ref: '#/components/schemas/IrnRefundRequestId'

    RefundSuccessResponse:
      type: object
      properties:
        payuPaymentReference:
          $ref: '#/components/schemas/PayuPaymentReference'
        code:
          type: number
          enum: [200]
        message:
          type: string
          enum: ["Confirmed", "Order already confirmed"]

    2xxResponseCode:
        type: number
        enum: [200,202]
        description: "A Success code (http code that is also returned in headers)"

    4xxResponseCode:
        type: number
        enum: [400, 401, 403, 409, 404, 429]
        example: 400
        description: "A bad request code (http code that is also returned in headers)"

    404ResponseCode:
        type: number
        enum: [404]
        example: 404
        description: "Payment not found response"

    5xxResponseCode:
        type: number
        enum: [500, 502]
        example: 500
        description: "Some error occurred trying to process request (http code that is also returned in headers)"

    ResponseMessage:
      type: string
      example: "A text message with details about processing result or with some message error"
      description: "A text message with details about processing result or with some message error"

    ClientErrorResponseMessage:
      type: string
      example: "Parameter 'x' must be a string"
      description: "A text message with details about the client error"

    PaginationPrev:
      type: string
      example: "/v4/payout?startDate=2021-04-12T16:40:00-04:00&endDate=2021-04-17T16:40:00-04:00&page=1"
      description: "Get previous page with results"

    PaginationNext:
      type: string
      example: "/v4/payout?startDate=2021-04-12T16:40:00-04:00&endDate=2021-04-17T16:40:00-04:00&page=2"
      description: "Get next page with results"

    PaginationLast:
      type: string
      example: "/v4/payout?startDate=2021-04-12T16:40:00-04:00&endDate=2021-04-17T16:40:00-04:00&page=25"
      description: "Get last page with results"

    ErrorMessage:
      description: Reason why request failed.
      type: string
      example: "A text message with details about processing result or with some message error"

    InternalErrorMessage:
      description: Reason why request failed.
      type: string
      example: "A text message with details about processing result or with some message error"
      enum:
        - Internal server error

    InternalErrorStatus:
      type: string
      example: "A text representing the status of the response"
      enum:
        - INTERNAL_ERROR

    ClientResponseStatus:
      type: string
      example: "A text representing the status of the response"
      enum:
        - INVALID_ACCOUNT
        - REQUEST_EXPIRED
        - INPUT_ERROR
        - HASH_MISMATCH
        - DUPLICATE_ORDER
        - DIFFERENT_PRODUCT_ARRAY_COUNT
        - PRODUCT_INVALID_CODE
        - PRODUCT_INVALID_NAME
        - PRODUCT_INVALID_PRICE
        - PRODUCT_INVALID_VAT
        - DISCOUNT_NOT_SUPPORTED
        - SHIPPING_NOT_SUPPORTED
        - INVALID_TOKEN
        - INVALID_CC_TOKEN
        - INVALID_CAMPAIGN_TYPE
        - INVALID_CAMPAIGN_INSTALLMENTS
        - PRODUCT_INVALID_PRICE_TYPE
        - INVALID_CURRENCY
        - INVALID_CURRENCY_FOR_SELLER
        - INVALID_PRICE
        - INVALID_CUSTOMER_INFO
        - ORDER_TOO_OLD
        - INVALID_EXTERNAL_REFERENCE
        - INVALID_AIRLINE_INFO
        - ORDER_MAX_AMOUNT_EXCEEDED
        - INVALID_PAYMENT_INFO
        - WRONG_VERSION
        - ALREADY_AUTHORIZED
        - ALREADY_PENDING_AUTHORIZATION
        - AUTHORIZATION_ALREADY_IN_PROGRESS

    IdnResponseStatus:
      type: string
      example: "A text representing the status of the response"
      enum:
        - SUCCESS
        - MISSING_OR_INCORRECT_STRUCTURE_REFERENCE
        - MISSING_OR_INCORRECT_STRUCTURE_AMOUNT
        - MISSING_OR_INCORRECT_STRUCTURE_CURRENCY
        - ERROR_CONFIRMING_ORDER
        - ALREADY_CONFIRMED
        - REFERENCE_NOT_FOUND
        - INVALID_ORIGINAL_AMOUNT
        - INVALID_CURRENCY
        - INVALID_AMOUNT
        - INVALID_SIGNATURE
        - LIMIT_CALLS_EXCEEDED
        - INVALID_REQUEST
        - PARTIAL_AMOUNT_NOT_SUPPORTED
        - PRODUCTS_NOT_SUPPORTED
        - INVALID_CREDENTIALS
        - INTERNAL_ERROR
        - INVALID_REQUEST_STRUCTURE

    IrnResponseStatus:
      type: string
      example: "A text representing the status of the response"
      enum:
        - SUCCESS
        - MISSING_OR_INCORRECT_STRUCTURE_REFERENCE
        - MISSING_OR_INCORRECT_STRUCTURE_ORIGINAL_AMOUNT
        - MISSING_OR_INCORRECT_STRUCTURE_CURRENCY
        - INVALID_ORDER_STATE
        - ALREADY_CANCELLED
        - INTERNAL_ERROR
        - REFERENCE_NOT_FOUND
        - INVALID_ORIGINAL_AMOUNT
        - INVALID_CURRENCY
        - MISSING_OR_INCORRECT_STRUCTURE_AMOUNT
        - INVALID_AMOUNT
        - INVALID_CREDENTIALS
        - INVALID_PAYMENT_METHOD
        - INVALID_LOYALTY_POINTS
        - NOT_ENOUGH_LOYALTY_POINTS
        - LIMIT_CALLS_EXCEEDED
        - PRODUCTS_NOT_SUPPORTED_FOR_PARTIAL_IRN
        - INVALID_PRODUCTS
        - INVALID_REQUEST_STRUCTURE
        - INVALID_REQUEST
        - INVALID_PRODUCT_SKU
        - INVALID_PRODUCT_AMOUNT
        - INVALID_MARKETPLACE_FIELDS
        - INVALID_MARKETPLACE_COMMISSION
        - INVALID_MARKETPLACE_COMMISSION
        - INVALID_MARKETPLACE_FIELDS
        - INVALID_MARKETPLACE_PRODUCTS_STRUCTURE
        - INVALID_INSTALLMENTS_AMOUNT
        - INVALID_INSTALLMENTS_PRODUCT
        - INVALID_FAST_REFUND_PARAMETER
        - FAST_REFUND_NOT_AVAILABLE
        - IRN_ERROR_BOTH_PRODUCTS_AND_MARKETPLACE_V1_NOT_ALLOWED

    IrnRefundRequestId:
      description: 'Unique request identifier for IRN request. This field will not be sent unless your account is configured on our side to receive it. Please contact us for more information.'
      type: string
      example: "800d45c7-70c4-4107-ac7c-29bf03cdab63"

    NotFoundMessage:
      type: string
      example: "Payment not found"

    PayuPaymentReference:
      anyOf:
        - type: number
        - type: string
      format: integer
      example: 896782
      minimum: 0
      exclusiveMinimum: true

    MerchantPayoutReference:
      description: Only a-z, A-Z, 0-9, dash and underscore are allowed
      type: string
      example: "896782"
      minLength: 1

    PriceAmount:
      type: string
      format: double
      example: 10.50

    Currency:
      description: 'The currency code in which the prices are expressed. According to ISO 4217 (https://en.wikipedia.org/wiki/ISO_4217)'
      type: string
      example: EUR
      minLength: 1

    CreditLimit:
      type: object
      required:
        - currency
        - amount
      properties:
        currency:
          description: 'Currency limit. For now we support only account default currency.'
          type: string
          example: RON
        amount:
          description: 'Amount limit'
          type: number
          format: double
          example: 10.50

    StatusSuccessResponse:
      type: object
      properties:
        paymentStatus:
          $ref: '#/components/schemas/PaymentStatus'
        payuPaymentReference:
          $ref: '#/components/schemas/PayuPaymentReference'
        code:
          type: number
          enum:
            - 200
        message:
          type: string
          enum:
            - Success
        authorizations:
          type: array
          items:
            $ref: '#/components/schemas/AuthorizationResource'
        refunds:
            type: array
            items:
                $ref: '#/components/schemas/RefundResource'
        captures:
            type: array
            items:
                $ref: '#/components/schemas/CaptureResource'
    CardCvv:
      description: "The CCV/CVV2 code for the card (see https://en.wikipedia.org/wiki/Card_security_code). For some card types or based on merchant settings this can be empty, otherwise it should have a numerical value."
      anyOf:
        - type: integer
        - type: string
      example: 475

    CardOwner:
      description: 'The card owner name, as it appears on the card. If missing the firstName and lastName from billing will be consider'
      type: string
      example: John Doe

###Subnodes For Response
    PaymentStatus:
      type: string
      example: PAYMENT_AUTHORIZED
      enum: [IN_PROGRESS, REVERSED, CARD_NOTAUTHORIZED, WAITING_PAYMENT, COMPLETE, PAYMENT_AUTHORIZED, REFUND, CANCELED,
       CASH, TEST, FRAUD, INVALID]
      description: >
          Current payment status. Possible values:
            * `NOT_FOUND` - not existing/unfinished order
            * `WAITING_PAYMENT` - the order has been placed and payment is waiting
            * `CARD_NOTAUTHORIZED` - the card used for payment has not been authorized
            * `IN_PROGRESS` - payment has been authorized, the order is in approval process
            * `PAYMENT_AUTHORIZED` - payment authorized, order approved
            * `COMPLETE` - finished order (charged/delivered)
            * `FRAUD` - fraud suspect order
            * `INVALID` - invalid data entered by the customer
            * `TEST` - test order
            * `CASH` - order with cash on delivery
            * `REVERSED` - order reversed, money unlocked in the customer account
            * `REFUND` - order refund, returned to the customer account

    PaymentResult:
      type: object
      properties:
        payuResponseCode:
          type: string
          example: GWERROR_41
          description: | 
            PayU response message code. Important ones:
              * `AUTHORIZED` : Payment was authorized
              * `GWERROR_51` : Insufficient funds
              * `-8888` : Waiting for authorization. Merchants can rely on [IPN webhook](/docs/#tag/Webhooks/paths/~1merchant-ipn-url/post) 
            or [Status request](docs/#tag/Payment-API/paths/~1v4~1payments~1status~1{merchantPaymentReference}/get) to retrieve the authorization status.
              * [More codes here](/docs/#tag/Response-codes)
        authCode:
          type: string
          example: 324534
        rrn:
          type: string
          example: 43534654
        installmentsNumber:
          type: string
          example: 2

        bankResponseDetails:
          $ref: '#/components/schemas/BankResponseDetails'

        cardDetails:
          $ref: '#/components/schemas/CardResponseDetails'


        3dsDetails:
          $ref: '#/components/schemas/3dsResponseDetails'

        type:
          type: string
          enum: ['redirect', 'wire', 'offline']

        wireAccounts:
          type: array
          items:
            type: object
            properties:
              bankIdentifier:
                type: string
                example: BANN

              bankAccount:
                type: string
                example: 678819991

              routingNumber:
                nullable: true
                type: number
                format: int32
                example: 263181368

              ibanAccount:
                nullable: true
                type: string
                example: RO49AAAA1B31007593840000

              bankSwift:
                type: string
                example: UGBIROBU

              country:
                type: string
                example: RO

              recipientName:
                type: string
                example: My Company

              recipientVatId:
                type: string
                example: 1234567890

        url:
          description: "Merchant should redirect user to this url, so he can finish payment. Can be the url for beginning of 3dsecure process, for redirecting to the client bank or to a third-party wallet (e.g: BTPay)"
          type: string
          example: http://acquirer_url/test
        appDeepLinks:
          $ref: '#/components/schemas/AppDeepLinks'

    AuthorizationResource:
      type: object
      description: This node is sent by PayU with information on the used card
      required:
        - authorized
      properties:
        timestamp:
          description: "Datetime of the payment attempt"
          type: string
          format: ISO_8601 datetime
          example: '2022-01-02T12:00:14+00:00'
        authorized:
          type: string
          example: 'SUCCESS'
          enum:
            - SUCCESS
            - PENDING
            - FAILED
        credit:
          type: object
          properties:
            nrInstalments:
              anyOf:
                - type: integer
                - type: string
              example: 4
            financialPartner:
              type: string
              example: "PARTNER"
            campaignCode:
              type: string
              example: "CAMPAIGN01"
        cardDetails:
          type: object
          properties:
            cardScheme:
              type: string
              example: 'VISA'
              enum:
                - VISA
                - MASTERCARD
                - AMEX
                - TROY
                - MIR
                - UNIONPAY
                - OTHER
            cardType:
              type: string
              example: 'DEBIT'
              enum:
                - DEBIT
                - CREDIT
                - PREPAID
                - UNKNOWN
            issuerBank:
              type: string
              example: 'BRD Groupe Societe Generale'
              description: Name of the bank that issued the card
            issuerCountryCode:
              type: string
              example: RO
              description: ISO 3166-1 alpha-2 country code where the card was issued
            cardProfile:
              type: string
              example: 'CONSUMER'
              enum:
                - CONSUMER
                - COMMERCIAL
                - UNKNOWN
                - BOTH
            lastFourDigits:
              type: string
              example: "1111"
              description: Last 4 digits of the requested card
            binNumber:
              type: string
              example: "411111"
              description: BIN(first 6 digits) of the requested card
          required:
            - binNumber
            - lastFourDigits
        storedCredentials:
          $ref: '#/components/schemas/StoredCredentialsResponse'
        responseCode:
          type: string
          description: 'PayU message code (RETURN_CODE) on the reason for failure. It is sent only for orders that could not be authorized for various reasons'
          example: 'GWERROR_51'
        responseMessage:
          type: string
          description: 'An error message on the reason for failure. It is sent only for orders that could not be authorized for various reasons'
          example: 'Insufficient funds'
        merchantPaymentAttemptReference:
          type: string
          description: 'Payment attempt reference'
          example: '34dfsd-sdgds'
        commission:
          anyOf:
            - type: number
              format: double
            - type: string
          example: "25.10"
        bankCommission:
          anyOf:
            - type: number
              format: double
            - type: string
          example: "25.10"
        currency:
          type: string
          example: 'RON'
          description: The currency used to create the transaction
        amount:
          anyOf:
            - type: number
              format: double
            - type: string
          example: "352.30"
          description: Amount of the authorization
    RefundResource:
      required:
        - status
        - requestTimestamp
        - amount
        - currency
        - commission
        - refundRequestId
      type: object
      description: This node is sent by PayU with information on the refund
      properties:
        status:
          type: string
          example: 'REFUND'
          enum:
            - PENDING
            - REFUND
            - REVERSED
        merchantRefundReference:
          type: string
          example: '34dfsd-sdgds'
          description: 'Refund reference value that was sent during the refund request'
        requestTimestamp:
          description: "Datetime of when the refund request was received by PayU"
          type: string
          format: ISO_8601 datetime
          example: '2022-01-02T12:00:14+00:00'
        timestamp:
          description: "Datetime of the refund"
          type: string
          format: ISO_8601 datetime
          example: '2022-01-02T12:00:14+00:00'
        amount:
          anyOf:
            - type: number
              format: double
            - type: string
          example: "352.30"
          description: Amount of the refund
        currency:
          type: string
          example: 'RON'
          description: The currency used to create the transaction
        commission:
          anyOf:
            - type: number
              format: double
            - type: string
          example: "25.10"
        bankCommission:
          anyOf:
            - type: number
              format: double
            - type: string
          example: "25.10"
        rrn:
          type: string
          example: 43534654
        refundRequestId:
          type: string
          format: uuid
          example: '2149a875-8984-471a-b4a4-b74fa28b59ff'
          description: This contains the unique ID that was sent in the "Refund a payment" API response.
    CaptureResource:
      type: object
      description: This node is sent by PayU with information on the capture
      required:
        - status
        - amount
        - currency
        - commission
        - rrn
      properties:
        status:
          type: string
          example: 'COMPLETE'
          enum:
            - PENDING
            - COMPLETE
        requestTimestamp:
          description: "Datetime of when the capture request was received by PayU"
          type: string
          format: ISO_8601 datetime
          example: '2022-01-02T12:00:14+00:00'
        timestamp:
          description: "Datetime of the capture"
          type: string
          format: ISO_8601 datetime
          example: '2022-01-02T12:00:14+00:00'
        amount:
          anyOf:
            - type: number
              format: double
            - type: string
          example: "352.30"
          description: Amount of the capture
        currency:
          type: string
          example: 'RON'
          description: The currency used to create the transaction
        commission:
          anyOf:
            - type: number
              format: double
            - type: string
          example: "25.10"
        bankCommission:
          anyOf:
            - type: number
              format: double
            - type: string
          example: "25.10"
        rrn:
          type: string
          example: 43534654


    IpnOrderData:
      type: object
      description: This node is sent by PayU on the IPN request with information on the order
      required:
        - orderDate
        - payuPaymentReference
        - merchantPaymentReference
        - status
        - currency
        - amount
      properties:
        orderDate:
          type: string
          example: '2018-08-02T12:00:14+00:00'
          description: Date sent by the merchant when creating the payment in the ISO_8601 datetime format
        payuPaymentReference:
          type: string
          example: '6742343'
          description: Payment reference assigned by PayU to the payment
        merchantPaymentReference:
          $ref: '#/components/schemas/MerchantPaymentReference'
        status:
          type: string
          enum:
            - PAYMENT_AUTHORIZED
            - PAYMENT_RECEIVED
            - TEST
            - CASH
            - COMPLETE
            - REVERSED
            - REFUND
            - SUSPECT
            - PENDING
            - PROCESSING
            - INVALID
            - CARD_NOT_AUTHORIZED
            - -
          description: >
            Indicates the current status of the order for which the notification is sent.Possible values:
             * `PAYMENT_AUTHORIZED` - payment authorized, order approved
             * `PAYMENT_RECEIVED` - wired transfer payment is finished
             * `TEST` - test order
             * `CASH` - order with cash on delivery
             * `COMPLETE` - payment finished, delivery confirmed by merchant
             * `REVERSED` - order reversed, money unlocked in the customer account
             * `REFUND` - order refund, returned to the customer account
             * `SUSPECT` - fraud suspect order
             * `PENDING` - pending order waiting for approval
             * `PROCESSING` - payment has been authorized, the order is in approval process
             * `INVALID` - invalid data entered by the customer
             * `CARD_NOT_AUTHORIZED` - the card used for payment was not authorized
             * `-` - unfinished order
        currency:
          type: string
          example: 'RON'
          description: The currency used to create the transaction
        amount:
          anyOf:
            - type: number
              format: double
            - type: string
          example: "352.30"
          description: Original amount of the transaction (including installments cost if applicable)
        commission:
          anyOf:
            - type: number
              format: double
            - type: string
          example: "25.10"
        loyaltyPointsAmount:
          anyOf:
            - type: number
              format: double
            - type: string
        loyaltyPointsDetails:
          $ref: '#/components/schemas/IpnLoyaltyPointsDetails'
        refundInfo:
          $ref: '#/components/schemas/IPNOrderRefundInfo'
        refundRequestId:
          type: string
          format: uuid
          example: '2149a875-8984-471a-b4a4-b74fa28b59ff'
          description: |
            If the `status` is either `REFUND` or `REVERSED`, this contains the unique ID that was sent in the "Refund a payment" API response.
            Please refer to the ["Refund a payment"](#tag/Payment-API/paths/~1v4~1payments~1refund/post) documentation for more information regarding this value.

            This field will not be sent unless your account is configured on our side to receive it. Please contact us for more information.
    IPNOrderRefundInfo:
      type: object
      description: refund order detailed information
      properties:
        chargeback:
          type: string
          example: "the merchandise does not match the merchant's description."
          description: Chargeback reason of refund order.
    IpnLoyaltyPointsDetails:
      type: array
      description: This node is sent by PayU on the IPN request with information on loyatly points used
      items:
        type: object
        properties:
          type:
            type: string
            example: 'BNS'
          amount:
            anyOf:
              - type: number
              - type: string
            example: "5"
    IpnPaymentResult:
      type: object
      description: This node is sent by PayU on the IPN request with relevant payment information
      properties:
        paymentMethod:
          type: string
          example: 'CCVISAMC'
          description: Payment method used for the transaction. For Masterpass transactions it would be CCVISAMC|MASTERPASS
        paymentDate:
          type: string
          example: '2018-08-02T12:00:14+00:00'
          description: Date when the payment was processed in the ISO_8601 datetime format
        captureDate:
          type: string
          example: '2018-08-02T12:00:14+00:00'
          description: Date when the payment was processed in the ISO_8601 datetime format
        installmentsNumber:
          anyOf:
            - type: number
              format: integer
            - type: string
          example: "5"
        authCode:
          type: string
          example: 324534
        merchantId:
          type: string
          example: A891911
        rrn:
          type: string
          example: 43534654
        cardDetails:
         $ref: '#/components/schemas/IpnCardDetails'
        paymentBankShortName:
          type: string
          example: 'BRD'
        serviceProcessingType:
          type: string
          example: 'TSP'
    IpnCardDetails:
      type: object
      description: This node is sent by PayU on the IPN request with the relevant card data
      properties:
        bin:
          anyOf:
            - type: number
            - type: string
          example: "424242"
          description: First 6 numbers of the used card
        owner:
          type: string
          example: 'John Doe'
          description: Owner of the card as it appears on it.
        pan:
          type: string
          example: '4242-xxxx-xxxx-2466'
          description: Obfuscated card number
        type:
          type: string
          example: 'Visa'
          description: Card type
        cardIssuerBank:
          type: string
          example: 'EST'
    IpnClientData:
      type: object
      description: This node is sent by PayU on the IPN request with the relevant client data
      properties:
        billing:
         $ref: '#/components/schemas/Billing'
        delivery:
         $ref: '#/components/schemas/IpnDeliveryDetails'
        ip:
          type: string
          example: '192.168.24.1'
          description: IP address of the client
        ipCountry:
          type: string
          example: 'Romania'
          description: Associated country of the IP address
    IpnDeliveryDetails:
      type: object
      description: This node is sent by PayU on the IPN request with the identity data of the transaction
      properties:
        firstName:
          type: string
          example: 'John'
        lastName:
          type: string
          example: 'Doe'
        companyName:
          type: string
          example: 'Example Inc.'
        addressLine1:
          type: string
          example: 'example address 1'
        addressLine2:
          type: string
          example: 'example address 2'
        city:
          type: string
          example: 'Bucharest'
        state:
          type: string
          example: 'Ilfov'
        zipCode:
          type: string
          example: '900169'
        countryCode:
          type: string
          example: 'ro'
        phone:
          type: string
          example: '+407101082567'
        email:
          type: string
          example: 'example@email.com'
    IdentityDocument:
      description: "Identity document of the client."
      type: object
      properties:
        number:
          type: string
          example: 123445
          description: "Shopper's ID number (for the specified ID type)"
        type:
          description: "Shopper's ID type - mandatory for UPT"
          type: string
          example: PERSONALID
          enum:
            - PERSONALID
            - PASSPOR
            - DRVLICENSE
    IpnProducts:
      type: array
      items:
        type: object
        properties:
          name:
            type: string
            example: Product name
          sku:
            description: >-
              Sku of the product [see
              wiki](https://en.wikipedia.org/wiki/Stock_keeping_unit). Be aware
              that if PayU will receive same sku for different producuts of the
              same merchant last one will be consider in different area of the
              platform (including authorization)
            anyOf:
              - type: number
              - type: string
            example: Code_XYZ
          additionalDetails:
            description: Additional information about product.
            type: string
            example: Product additional information
          unitPrice:
            description: Unit price of the product
            anyOf:
              - type: number
                format: double
              - type: string
            example: "21"
          quantity:
            anyOf:
              - type: number
                format: integer
              - type: string
            example: "2"
          vatAmount:
            description: VAT amount of the product.
            anyOf:
              - type: number
              - type: string
            example: "12"

    BankResponseDetails:
      type: object
      properties:
        terminalId:
          type: string
          example: A123456789
          description: replaces value 'CLIENT_ID'
        response:
          type: object
          properties:

            code:
              type: string
              example: 00
              description: replaces plugin value 'bankErrorCode'
            message:
              type: string
              example: Payment authorized
              description: replaces plugin value 'bankErrorMessage'
            status:
              type: string
              example: Authorized
              description: replace plugin value 'RESPONSE'
        hostRefNum:
          type: string
          example: 80001719289129

        merchantId:
          type: string
          example: A891911

        shortName:
          type: string
          example: UGBI
          description: replaces plugin value `TERMINAL`

        txRefNo:
          type: string
          example: O176721881

        oid:
          type: string
          example: A9891919911

        transId:
          type: string
          example: example

        customBankNode:
          type: object
          properties:
            qr:
              type: string
              description: Base64 encoded QR image
            url:
              type: string
              description: The URL contained in the QR image
          description: This node is FASTER_PAYMENTS payment method specific. Note that the QR expires after 20 minutes.
    CardResponseDetails:
      type: object
      properties:
        pan:
          type: string
          example: 411111******1111
        expiryYear:
          type: string
          example: 2026
        expiryMonth:
          type: string
          example: 07
    3dsResponseDetails:
      type: object
      properties:
        mdStatus: # 3ds
          type: string
          example: Y

        errorMessage: # 3ds
          type: string
          example: Some error message

        txStatus: # 3ds
          type: string
          example: Authorized

        xid: # 3ds
          type: string
          example: 78199a88871e0f00

        eci: #3ds
          type: number
          format: integer
          enum: [0,1,2,3,4,5,6,7]

        cavv: #3ds
          type: number
          format: integer
          example: 123

    AppDeepLinks:
      type: object
      description:
        Appears for some payment methods type, e.g. BTPay <br />
        This node enables app deep linking functionality. If supported by the merchant, it allows redirecting users directly to the appropriate mobile application based on their device, instead of a standard web redirect. 
        The merchant is expected to detect the user’s device and use the most relevant deep link provided in this node.
        If the merchant does not support this functionality or the user's device was not detected, it should fall back to the default behavior — redirecting users to the url parameter via a standard web redirect.
      properties:
        android:
          type: string
          example: "http://acquirer_url/test"

###End subnodes For Response

    MerchantPaymentReference:
      description: Payment reference in Merchant's system.
      anyOf:
        - type: string
        - type: number
      example: 34dfsd-sdgds

    MerchantPaymentAttemptReference:
      description: Payment attempt reference, which is unique in Merchant's system.
      anyOf:
        - type: string
        - type: number
      example: fj2930-kp38ls
      maxLength: 100

    ReturnUrl:
      description: 'Return URL on the Merchant webshop side that will be used in case of 3DS enrolled cards authorizations or for Pay By Link (PBL) payment methods after the payment attempt. If missing the merchant url setup on his PayU account will be used. The PayU will submit to this endpoint a form with four inputs: body, merchant, date and signature. For signature the same algorithm as for inline request will be used, but use data from form inputs '
      type: string
      nullable: true
      example: 'https://www.example.com/confirm'

    Payment_with_payment_page:
      type: object
      properties:
        merchantPaymentReference:
          $ref: '#/components/schemas/MerchantPaymentReference'
        merchantPaymentAttemptReference:
          $ref: '#/components/schemas/MerchantPaymentAttemptReference'
        currency:
          $ref: '#/components/schemas/Currency'
        returnUrl:
          $ref: '#/components/schemas/ReturnUrl'
        authorization:
          $ref: '#/components/schemas/authorization_with_payment_page'
        client:
          $ref: '#/components/schemas/Client'
        products:
          $ref: '#/components/schemas/Products'
        airlineInfo:
          $ref: '#/components/schemas/AirlineInfo'
        storedCredentials:
          $ref: '#/components/schemas/StoredCredentials'
        notification:
          $ref: '#/components/schemas/NotificationOptions'
        additionalDetails:
          $ref: '#/components/schemas/AdditionalDetails'
      required:
      - merchantPaymentReference
      - currency
      - client
      - products
      - authorization

    Payment_with_direct_card:
      type: object
      properties:
        merchantPaymentReference:
          $ref: '#/components/schemas/MerchantPaymentReference'
        merchantPaymentAttemptReference:
          $ref: '#/components/schemas/MerchantPaymentAttemptReference'
        currency:
          $ref: '#/components/schemas/Currency'
        returnUrl:
          $ref: '#/components/schemas/ReturnUrl'
        authorization:
          $ref: '#/components/schemas/authorization_with_direct_card'
        client:
          $ref: '#/components/schemas/Client'
        products:
          $ref: '#/components/schemas/Products'
        airlineInfo:
          $ref: '#/components/schemas/AirlineInfo'
        threeDSecure:
          $ref: '#/components/schemas/ThreeDSecure'
        storedCredentials:
          $ref: '#/components/schemas/StoredCredentials'
        notification:
          $ref: '#/components/schemas/NotificationOptions'
        additionalDetails:
          $ref: '#/components/schemas/AdditionalDetails'
      required:
        - merchantPaymentReference
        - currency
        - client
        - products
        - authorization

    Payment_with_merchant_token:
      type: object
      properties:
        merchantPaymentReference:
          $ref: '#/components/schemas/MerchantPaymentReference'
        merchantPaymentAttemptReference:
          $ref: '#/components/schemas/MerchantPaymentAttemptReference'
        currency:
          $ref: '#/components/schemas/Currency'
        returnUrl:
          $ref: '#/components/schemas/ReturnUrl'
        authorization:
          $ref: '#/components/schemas/authorization_with_merchant_token'
        client:
          $ref: '#/components/schemas/Client'
        products:
          $ref: '#/components/schemas/Products'
        airlineInfo:
          $ref: '#/components/schemas/AirlineInfo'
        threeDSecure:
          $ref: '#/components/schemas/ThreeDSecure'
        storedCredentials:
          $ref: '#/components/schemas/StoredCredentials'
        notification:
          $ref: '#/components/schemas/NotificationOptions'
        additionalDetails:
          $ref: '#/components/schemas/AdditionalDetails'
      required:
        - merchantPaymentReference
        - currency
        - client
        - products
        - authorization

    Payment_with_network_token:
      type: object
      properties:
        merchantPaymentReference:
          $ref: '#/components/schemas/MerchantPaymentReference'
        merchantPaymentAttemptReference:
          $ref: '#/components/schemas/MerchantPaymentAttemptReference'
        currency:
          $ref: '#/components/schemas/Currency'
        returnUrl:
          $ref: '#/components/schemas/ReturnUrl'
        authorization:
          $ref: '#/components/schemas/authorization_with_network_token'
        client:
          $ref: '#/components/schemas/Client'
        products:
          $ref: '#/components/schemas/Products'
        airlineInfo:
          $ref: '#/components/schemas/AirlineInfo'
        threeDSecure:
          $ref: '#/components/schemas/ThreeDSecure'
        storedCredentials:
          $ref: '#/components/schemas/StoredCredentials'
        notification:
          $ref: '#/components/schemas/NotificationOptions'
        additionalDetails:
          $ref: '#/components/schemas/AdditionalDetails'
      required:
        - merchantPaymentReference
        - currency
        - client
        - products
        - authorization

    Payment_with_google_pay_token:
      type: object
      properties:
        merchantPaymentReference:
          $ref: '#/components/schemas/MerchantPaymentReference'
        merchantPaymentAttemptReference:
          $ref: '#/components/schemas/MerchantPaymentAttemptReference'
        currency:
          $ref: '#/components/schemas/Currency'
        returnUrl:
          $ref: '#/components/schemas/ReturnUrl'
        authorization:
          $ref: '#/components/schemas/authorization_with_google_pay_token'
        client:
          $ref: '#/components/schemas/Client'
        products:
          $ref: '#/components/schemas/Products'
        airlineInfo:
          $ref: '#/components/schemas/AirlineInfo'
        threeDSecure:
          $ref: '#/components/schemas/ThreeDSecure'
        storedCredentials:
          $ref: '#/components/schemas/StoredCredentials'
        notification:
          $ref: '#/components/schemas/NotificationOptions'
        additionalDetails:
          $ref: '#/components/schemas/AdditionalDetails'
      required:
        - merchantPaymentReference
        - currency
        - client
        - products
        - authorization

    Payment_with_apple_pay_token:
      type: object
      properties:
        merchantPaymentReference:
          $ref: '#/components/schemas/MerchantPaymentReference'
        merchantPaymentAttemptReference:
          $ref: '#/components/schemas/MerchantPaymentAttemptReference'
        currency:
          $ref: '#/components/schemas/Currency'
        returnUrl:
          $ref: '#/components/schemas/ReturnUrl'
        authorization:
          $ref: '#/components/schemas/authorization_with_apple_pay_token'
        client:
          $ref: '#/components/schemas/Client'
        products:
          $ref: '#/components/schemas/Products'
        airlineInfo:
          $ref: '#/components/schemas/AirlineInfo'
        threeDSecure:
          $ref: '#/components/schemas/ThreeDSecure'
        storedCredentials:
          $ref: '#/components/schemas/StoredCredentials'
        notification:
          $ref: '#/components/schemas/NotificationOptions'
        additionalDetails:
          $ref: '#/components/schemas/AdditionalDetails'
      required:
        - merchantPaymentReference
        - currency
        - client
        - products
        - authorization

    Payment_with_one_time_use_token:
      type: object
      properties:
        merchantPaymentReference:
          $ref: '#/components/schemas/MerchantPaymentReference'
        merchantPaymentAttemptReference:
          $ref: '#/components/schemas/MerchantPaymentAttemptReference'
        currency:
          $ref: '#/components/schemas/Currency'
        returnUrl:
          $ref: '#/components/schemas/ReturnUrl'
        authorization:
          $ref: '#/components/schemas/authorization_with_one_time_use_token'
        client:
          $ref: '#/components/schemas/Client'
        products:
          $ref: '#/components/schemas/Products'
        airlineInfo:
          $ref: '#/components/schemas/AirlineInfo'
        storedCredentials:
          $ref: '#/components/schemas/StoredCredentials'
        notification:
          $ref: '#/components/schemas/NotificationOptions'
        additionalDetails:
          $ref: '#/components/schemas/AdditionalDetails'
      required:
        - merchantPaymentReference
        - currency
        - client
        - products
        - authorization

    Payment_with_BT24_internet_banking:
      type: object
      properties:
        merchantPaymentReference:
          $ref: '#/components/schemas/MerchantPaymentReference'
        merchantPaymentAttemptReference:
          $ref: '#/components/schemas/MerchantPaymentAttemptReference'
        currency:
          $ref: '#/components/schemas/Currency'
        returnUrl:
          $ref: '#/components/schemas/ReturnUrl'
        authorization:
          $ref: '#/components/schemas/authorization_with_BT24_internet_banking'
        client:
          $ref: '#/components/schemas/Client'
        products:
          $ref: '#/components/schemas/Products'
        airlineInfo:
          $ref: '#/components/schemas/AirlineInfo'
        storedCredentials:
          $ref: '#/components/schemas/StoredCredentials'
        notification:
          $ref: '#/components/schemas/NotificationOptions'
        additionalDetails:
          $ref: '#/components/schemas/AdditionalDetails'
      required:
        - merchantPaymentReference
        - currency
        - client
        - products
        - authorization

    Payment_with_wire_transfer:
      type: object
      properties:
        merchantPaymentReference:
          $ref: '#/components/schemas/MerchantPaymentReference'
        merchantPaymentAttemptReference:
          $ref: '#/components/schemas/MerchantPaymentAttemptReference'
        currency:
          $ref: '#/components/schemas/Currency'
        returnUrl:
          $ref: '#/components/schemas/ReturnUrl'
        authorization:
          $ref: '#/components/schemas/authorization_with_wire_transfer'
        client:
          $ref: '#/components/schemas/Client'
        products:
          $ref: '#/components/schemas/Products'
        airlineInfo:
          $ref: '#/components/schemas/AirlineInfo'
        storedCredentials:
          $ref: '#/components/schemas/StoredCredentials'
        notification:
          $ref: '#/components/schemas/NotificationOptions'
        additionalDetails:
          $ref: '#/components/schemas/AdditionalDetails'
      required:
        - merchantPaymentReference
        - currency
        - client
        - products
        - authorization

    Payment_with_open_banking:
      type: object
      properties:
        merchantPaymentReference:
          $ref: '#/components/schemas/MerchantPaymentReference'
        merchantPaymentAttemptReference:
          $ref: '#/components/schemas/MerchantPaymentAttemptReference'
        currency:
          $ref: '#/components/schemas/Currency'
        returnUrl:
          $ref: '#/components/schemas/ReturnUrl'
        authorization:
          $ref: '#/components/schemas/authorization_with_open_banking'
        client:
          $ref: '#/components/schemas/Client'
        products:
          $ref: '#/components/schemas/Products'
        airlineInfo:
          $ref: '#/components/schemas/AirlineInfo'
        storedCredentials:
          $ref: '#/components/schemas/StoredCredentials'
        notification:
          $ref: '#/components/schemas/NotificationOptions'
        additionalDetails:
          $ref: '#/components/schemas/AdditionalDetails'
      required:
        - merchantPaymentReference
        - currency
        - client
        - products
        - authorization
    Payment_with_btpay:
      type: object
      properties:
        merchantPaymentReference:
          $ref: '#/components/schemas/MerchantPaymentReference'
        merchantPaymentAttemptReference:
          $ref: '#/components/schemas/MerchantPaymentAttemptReference'
        currency:
          $ref: '#/components/schemas/Currency'
        returnUrl:
          $ref: '#/components/schemas/ReturnUrl'
        authorization:
          $ref: '#/components/schemas/authorization_with_btpay'
        client:
          $ref: '#/components/schemas/Client'
        products:
          $ref: '#/components/schemas/Products'
        airlineInfo:
          $ref: '#/components/schemas/AirlineInfo'
        storedCredentials:
          $ref: '#/components/schemas/StoredCredentials'
        notification:
          $ref: '#/components/schemas/NotificationOptions'
        additionalDetails:
          $ref: '#/components/schemas/AdditionalDetails'
      required:
        - merchantPaymentReference
        - currency
        - client
        - products
        - authorization

    ###subnodes for request
    authorization_with_payment_page:
      description: 'This node contains information about how to authorize the payment.'
      type: object
      required:
        - paymentMethod
        - usePaymentPage
      properties:
        paymentMethod:
          type: string
          enum:
          - CCVISAMC
          - CARD_AVANTAJ
          - STAR_BT
          - UNICREDIT
          - BRD_INSTALLMENTS
          - RAIFFEISEN
          - GARANTI_RO
          - BCR_INSTALLMENTS
          - ALPHABANK_INSTALLMENTS
          - OPTIMO
          - CARD_EMAG
#          - ITRANSFER_BT
#          - CREDIT_SLICE
#          - CREDIT_BUY_NOW_PAY_LATER
#          - WIRE
        usePaymentPage:
          description: |
            The ALU call will return a redirect URL to the payment page, to allow the client to enter card data.
          type: string
          enum: ['YES']
        paymentPageOptions:
          $ref: '#/components/schemas/PaymentPageOptions'
        installmentsNumber:
          $ref: '#/components/schemas/InstallmentsNumber'
        installmentOptions:
          $ref: '#/components/schemas/InstallmentOptions'
        useLoyaltyPoints:
          $ref: '#/components/schemas/UseLoyaltyPoints'
        loyaltyPointsAmount:
          $ref: '#/components/schemas/LoyaltyPointsAmount'
        campaignType:
          type: string
          enum: [EXTRA_INSTALLMENTS, DELAY_INSTALLMENTS]
        fx:
          $ref: '#/components/schemas/Fx'

    authorization_with_direct_card:
      description: 'This node contains information about how to authorize the payment.'
      type: object
      required:
        - paymentMethod
        - cardDetails
      properties:
        paymentMethod:
          type: string
          enum:
            - CCVISAMC
            - CARD_AVANTAJ
            - STAR_BT
            - UNICREDIT
            - BRD_INSTALLMENTS
            - RAIFFEISEN
            - GARANTI_RO
            - BCR_INSTALLMENTS
            - ALPHABANK_INSTALLMENTS
            - OPTIMO
            - CARD_EMAG
#            - ITRANSFER_BT
#            - CREDIT_SLICE
#            - CREDIT_BUY_NOW_PAY_LATER
#            - WIRE
        cardDetails:
          $ref: '#/components/schemas/CardDetails'
        installmentsNumber:
          $ref: '#/components/schemas/InstallmentsNumber'
        useLoyaltyPoints:
          $ref: '#/components/schemas/UseLoyaltyPoints'
        loyaltyPointsAmount:
          $ref: '#/components/schemas/LoyaltyPointsAmount'
        campaignType:
          type: string
          enum: [EXTRA_INSTALLMENTS, DELAY_INSTALLMENTS]
        fx:
          $ref: '#/components/schemas/Fx'

    authorization_with_merchant_token:
      description: 'This node contains information about how to authorize the payment.'
      type: object
      required:
        - paymentMethod
        - merchantToken
      properties:
        paymentMethod:
          type: string
          enum:
            - CCVISAMC
            - CARD_AVANTAJ
            - STAR_BT
            - UNICREDIT
            - BRD_INSTALLMENTS
            - RAIFFEISEN
            - GARANTI_RO
            - BCR_INSTALLMENTS
            - ALPHABANK_INSTALLMENTS
            - OPTIMO
            - CARD_EMAG
#            - ITRANSFER_BT
            - CREDIT_SLICE
            - CREDIT_BUY_NOW_PAY_LATER
#            - WIRE
        merchantToken:
          $ref: '#/components/schemas/MerchantToken'
        credit:
          $ref: '#/components/schemas/CreditDetails'
        installmentsNumber:
          $ref: '#/components/schemas/InstallmentsNumber'
        useLoyaltyPoints:
          $ref: '#/components/schemas/UseLoyaltyPoints'
        loyaltyPointsAmount:
          $ref: '#/components/schemas/LoyaltyPointsAmount'
        campaignType:
          type: string
          enum: [EXTRA_INSTALLMENTS, DELAY_INSTALLMENTS]
        fx:
          $ref: '#/components/schemas/Fx'

    authorization_with_network_token:
      description: 'This node contains information about how to authorize the payment.'
      type: object
      required:
        - paymentMethod
        - networkToken
      properties:
        paymentMethod:
          type: string
          enum:
            - CCVISAMC
        networkToken:
          $ref: '#/components/schemas/NetworkToken'
        installmentsNumber:
          $ref: '#/components/schemas/InstallmentsNumber'
        useLoyaltyPoints:
          $ref: '#/components/schemas/UseLoyaltyPoints'
        loyaltyPointsAmount:
          $ref: '#/components/schemas/LoyaltyPointsAmount'
        campaignType:
          type: string
          enum: [EXTRA_INSTALLMENTS, DELAY_INSTALLMENTS]
        fx:
          $ref: '#/components/schemas/Fx'

    authorization_with_google_pay_token:
      description: 'This node contains information about how to authorize the payment.'
      type: object
      required:
        - paymentMethod
        - googlePayToken
      properties:
        paymentMethod:
          type: string
          enum:
            - CCVISAMC
        googlePayToken:
          $ref: '#/components/schemas/GooglePayToken'
        installmentsNumber:
          $ref: '#/components/schemas/InstallmentsNumber'
        useLoyaltyPoints:
          $ref: '#/components/schemas/UseLoyaltyPoints'
        loyaltyPointsAmount:
          $ref: '#/components/schemas/LoyaltyPointsAmount'
        campaignType:
          type: string
          enum: [EXTRA_INSTALLMENTS, DELAY_INSTALLMENTS]
        fx:
          $ref: '#/components/schemas/Fx'

    authorization_with_apple_pay_token:
      description: 'This node contains information about how to authorize the payment.'
      type: object
      required:
        - paymentMethod
        - applePayToken
      properties:
        paymentMethod:
          type: string
          enum:
            - CCVISAMC
        applePayToken:
          $ref: '#/components/schemas/ApplePayToken'
        installmentsNumber:
          $ref: '#/components/schemas/InstallmentsNumber'
        useLoyaltyPoints:
          $ref: '#/components/schemas/UseLoyaltyPoints'
        loyaltyPointsAmount:
          $ref: '#/components/schemas/LoyaltyPointsAmount'
        campaignType:
          type: string
          enum: [EXTRA_INSTALLMENTS, DELAY_INSTALLMENTS]
        fx:
          $ref: '#/components/schemas/Fx'

    authorization_with_one_time_use_token:
      description: 'This node contains information about how to authorize the payment.'
      type: object
      required:
        - paymentMethod
        - oneTimeUseToken
      properties:
        paymentMethod:
          type: string
          enum:
            - CCVISAMC
        oneTimeUseToken:
          $ref: '#/components/schemas/OneTimeUseToken'
        installmentsNumber:
          $ref: '#/components/schemas/InstallmentsNumber'
        useLoyaltyPoints:
          $ref: '#/components/schemas/UseLoyaltyPoints'
        loyaltyPointsAmount:
          $ref: '#/components/schemas/LoyaltyPointsAmount'
        campaignType:
          type: string
          enum: [EXTRA_INSTALLMENTS, DELAY_INSTALLMENTS]
        fx:
          $ref: '#/components/schemas/Fx'

    authorization_with_wire_transfer:
      description: 'This node contains information about how to authorize the payment.'
      type: object
      required:
        - paymentMethod
      properties:
        paymentMethod:
          type: string
          enum:
            - WIRE
        installmentsNumber:
          $ref: '#/components/schemas/InstallmentsNumber'
        useLoyaltyPoints:
          $ref: '#/components/schemas/UseLoyaltyPoints'
        loyaltyPointsAmount:
          $ref: '#/components/schemas/LoyaltyPointsAmount'
        campaignType:
          type: string
          enum: [EXTRA_INSTALLMENTS, DELAY_INSTALLMENTS]
        fx:
          $ref: '#/components/schemas/Fx'

    authorization_with_BT24_internet_banking:
      type: object
      required:
        - paymentMethod
      properties:
        paymentMethod:
          type: string
          enum:
            - ITRANSFER_BT
        installmentsNumber:
          $ref: '#/components/schemas/InstallmentsNumber'
        useLoyaltyPoints:
          $ref: '#/components/schemas/UseLoyaltyPoints'
        loyaltyPointsAmount:
          $ref: '#/components/schemas/LoyaltyPointsAmount'
        campaignType:
          type: string
          enum: [EXTRA_INSTALLMENTS, DELAY_INSTALLMENTS]
        fx:
          $ref: '#/components/schemas/Fx'

    authorization_with_open_banking:
      description: 'This node contains information about how to authorize the payment.'
      type: object
      required:
        - paymentMethod
        - openBanking
      properties:
        paymentMethod:
          type: string
          enum: [ OPEN_BANKING ]
          description: Payment method identifier. Must be 'OPEN_BANKING' for this schema.
        openBanking:
          type: object
          required:
            - bank
          properties:
            bank:
              type: string
              description: |
                The code of the bank selected by the customer.
                Must match one of the supported Open Banking banks.
              enum:
                - BT_RO
                - BCR_RO
                - ING_RO
                - RAIF_RO
                - BRD_RO
                - UNICREDIT_RO
        installmentsNumber:
          $ref: '#/components/schemas/InstallmentsNumber'
        useLoyaltyPoints:
          $ref: '#/components/schemas/UseLoyaltyPoints'
        loyaltyPointsAmount:
          $ref: '#/components/schemas/LoyaltyPointsAmount'
        campaignType:
          type: string
          enum: [ EXTRA_INSTALLMENTS, DELAY_INSTALLMENTS ]
        fx:
          $ref: '#/components/schemas/Fx'

    authorization_with_btpay:
      description: 'This node contains information about how to authorize the payment.'
      type: object
      required:
        - paymentMethod
      properties:
        paymentMethod:
          type: string
          enum: [ BTPAY ]
          description: Payment method identifier. Must be 'BTPAY' for this schema.

    NetworkToken:
      description: |
        The `NetworkToken` node represents a tokenized card number used for secure digital transactions. This node supports the following types of tokens:
        - Network Token
        - Google Pay DPAN (Device Primary Account Number)
        - Apple Pay DPAN (Device Primary Account Number)
        **Note:* Only DPANs are supported in this node. FPANs (Funding Primary Account Numbers) are not supported.
      type: object
      required:
        - tokenType
        - number
        - expiryMonth
        - expiryYear
      properties:
        tokenType:
          type: string
          enum:
            - 'NETWORK_TOKEN'
            - 'APPLEPAY'
            - 'GOOGLEPAY_DPAN'
        number:
          description: The network token used for the payment
          type: string
          minLength: 12
          maxLength: 19
          example: 5181510361644410
        expiryMonth:
          description: The month in which the network token used expires
          anyOf:
            - type: integer
            - type: string
          minimum: 1
          maximum: 12
          example: 12
        expiryYear:
          description: The year in which the network token used expires
          anyOf:
            - type: integer
            - type: string
          maximum: 9999
          example: 2024
        owner:
          $ref: '#/components/schemas/CardOwner'
        cryptogram:
          description: The cryptographic value used to secure the transaction, ensuring the integrity and authenticity of the payment data.
          type: string
          example: 'ABCD1234EFGH5678'
        eci:
          description: The Electronic Commerce Indicator (ECI) value used to determine the level of security for the transaction.
          type: string
          example: '05'

    InstallmentsNumber:
      anyOf:
        - type: number
          format: integer
        - type: string
      example: 5

    InstallmentOptions:
      type: array
      items:
        type: object
        properties:
          programName:
            type: string
            example: STAR_BT
            description: The name of the card program that allows using installments.
              This value is the same as the cardProgram that the platform is returning on Card Info API.
                E.g. `STAR_BT`
          allowedInstallmentsNumber:
            type: array
            description: These values will be used to create an intersection between the current possible installment numbers defined on one's account and the values sent in this array.
              The resulting list will show in the payment page as the actual values allowed to be chosen from as an installment number for the transaction.
              E.g. `[3, 4, 6]`
            example: [3, 4, 6]
            items:
              type: number
              format: integer

    UseLoyaltyPoints:
      description: |
        The order will be paid using loyalty points.
        It can be used for one time payments and (only when the `loyaltyPointsAmount` parameter is set and smaller than order total amount) also for installments payments.
      type: string
      enum: ['YES', 'NO']

    LoyaltyPointsAmount:
      type: number
      description: |
        Indicates the money amount worth of loyalty points to be used for payment.
        It can be used only together with `useLoyaltyPoints` parameter (set to YES).
        It can be an integer that will represent the money amount.<br/>
        Please note that in case of Garanti cards, you can optionaly send multiple points information, since the bank supports multiple loyalty programs (BNS or FBB), but if you decide to sent an integer value, the system will default on the BNS program:
         - E.g using integer: `"loyaltyPointsAmount" : 16`
         - E.g using multiple loyaltyPoints: `"loyaltyPointsAmount" : { "FBB" : 12, "BNS" : 13 }`
        
        The value that you are sending (or the sum of values in the case of an array) should be less or equal to the money amount worth of loyalty points which you have available at the bank, otherwise, you will receive an error and the order will not be authorized.
      example: 3

    Client:
      description: 'Information about payer. If delivery information is missing, same as billing will be consider'
      type: object
      properties:
        billing:
          $ref: '#/components/schemas/Billing'
        delivery:
          $ref: '#/components/schemas/Delivery'
        ip:
          description: "Client browser IP. Must be a valid IP, otherwise request will fail "
          type: string
          format: ip
          example: 127.0.0.1
        time:
          description: "Client time from his browser. Format is: Y-M-D h:i:s"
          type: string
          example: '2018-07-15 13:01:23'
        communicationLanguage:
          type: string
          description: 'Will be used for client-facing messages (notification emails, payments pages). If is not specified or language is unavailable in PayU system, the default language will be used (RO)'
          enum: ['RO', 'EN', 'HU', 'BG', 'EL', 'ro', 'en', 'hu', 'bg', 'el']
          example: 'EN'
      required:
      - billing
    Billing:
      description: 'Billing information of the client (shopper) '
      type: object
      properties:
        firstName:
          description: Shopper's first name
          type: string
          example: John
        lastName:
          description: Shopper's first name
          type: string
          example: Doe
        email:
          description: Shopper's email
          type: string
          example: test@payu.ro
        countryCode:
          type: string
          example:
            RO
        phone:
          description: Shopper's phone number
          type: string
          example: 0771346934
        city:
          description: Shopper's city name
          type: string
          example: Bucharest
        state:
          type: string
          example: Bucharest
          nullable: true
        companyName:
          type: string
          example: PayU
          nullable: true
        taxId:
          description: "Tax id of the company (or fiscalCode)"
          type: string
          example: example
          nullable: true
        addressLine1:
          type: string
          example: example
          nullable: true
        addressLine2:
          type: string
          example: example
          nullable: true
        zipCode:
          type: string
          example: example
          nullable: true
        identityDocument:
         $ref: '#/components/schemas/IdentityDocument'
      required:
      - firstName
      - lastName
      - email
      - countryCode
      - phone
    Delivery:
      type: object
      properties:
        firstName:
          type: string
          example: John
        lastName:
          type: string
          example: Doe
        phone:
          type: string
          example: 40898625
        addressLine1:
          type: string
          example: example
        addressLine2:
          type: string
          example: example
        zipCode:
          type: string
          example: example
        city:
          type: string
          example: Bucharest
        state:
          type: string
          example: Bucharest
        countryCode:
          type: string
          example: RO
        email:
          type: string
          example: name@example.com
    Products:
      type: array
      items:
        type: object
        properties:
          name:
            type: string
            example: Product name
          sku:
            description: Sku of the product [see wiki](https://en.wikipedia.org/wiki/Stock_keeping_unit).
              Be aware that if PayU will receive same sku for different producuts of the same merchant last one will be consider in different area of the platform (including authorization)
            anyOf:
              - type: integer
              - type: string
            example: Code_XYZ
          additionalDetails:
            description: Additional information about product.
            type: string
            example: Product additional information
            nullable: true
          unitPrice:
            description: Unit price of the product
            anyOf:
              - type: number
              - type: string
            format: double
            example: 21.0
          quantity:
            anyOf:
              - type: number
              - type: string
            example: 2
          vat:
            description: "Vat of the product. Must exist on PayU platform, otherwise will be ignored."
            anyOf:
              - type: number
              - type: string
            example: '12'
          marketplace:
            $ref: '#/components/schemas/Marketplace'
        required:
        - name
        - sku
        - unitPrice
        - quantity

    Marketplace:
      description: "Mandatory for payment using [Marketplace Flow](#section/Overview/Marketplace-payment-flow)"
      type: object
      discriminator:
        propertyName: version
        mapping:
          '2.0': '#/components/schemas/MarketplaceV2Object'
          '1.0': '#/components/schemas/MarketplaceV1Object'
      anyOf:
        - $ref: '#/components/schemas/MarketplaceV2Object'
        - $ref: '#/components/schemas/MarketplaceV1Object'

    MarketplaceV1Object:
      properties:
        version:
          $ref: '#/components/schemas/MarketplaceVersion'
        merchantCode:
          $ref: '#/components/schemas/MerchantCode'
      required:
        - version
        - merchantCode

    MarketplaceV2Object:
      properties:
        version:
          $ref: '#/components/schemas/MarketplaceVersion'
        id:
          type: string
          format: uuid
          example: 49a88d24-7615-11e8-adc0-fa7ae01bbebc
          description: "Id of marketplace product. For refund must be id of initial product"
        sellerId:
          description: "ID of marketplace seller generated through *Marketplace::create seller* API"
          type: string
          format: uuid
          example: 7cff8d290e58-b4de-4c31-ac82-ac1ae54c
        commissionAmount:
          type: number
          format: double
          example: 1.66
        commissionCurrency:
          $ref: '#/components/schemas/Currency'
      required:
        - sellerId
        - commissionAmount
        - commissionCurrency
        - id

    MarketplaceCaptureObject:
      description: "Mandatory for payment using [Marketplace V2 Flow](#section/Overview/Marketplace-payment-flow)"
      properties:
        id:
          type: string
          format: uuid
          example: 49a88d24-7615-11e8-adc0-fa7ae01bbebc
          description: "Id of marketplace product. For refund must be id of initial product"
        sellerId:
          description: "ID of marketplace seller generated through *Marketplace::create seller* API"
          type: string
          format: uuid
          example: 7cff8d290e58-b4de-4c31-ac82-ac1ae54c
        commissionAmount:
          type: number
          format: double
          example: 1.66
        commissionCurrency:
          $ref: '#/components/schemas/Currency'
      required:
        - sellerId
        - commissionAmount
        - commissionCurrency
        - id

    AirlineInfo:
      type: object
      properties:
        passengerName:
          maxLength: 20
          description: First name and last name of the passenger
          type: string
          example: John Doe
        ticketNumber:
          description: Ticket number
          maxLength: 14
          type: string
          example: 348943
        refundPolicy:
          description: 'Possibility of refund (0 - no restrictions, 1 - non refundable)'
          maxLength: 1
          type: integer
          example: 1
        reservationSystem:
          description: 'Name of reservation system (e.g. ATS = Delta, SABR = Sabre)'
          maxLength: 4
          type: string
          example: ATS
        travelAgency:
          type: object
          properties:
            code:
              description: The code of travel agency
              maxLength: 8
              type: string
              example: TRVSMT
            name:
              description: The name of travel agency
              maxLength: 25
              type: string
              example: Travel Smart
        flightSegments:
          type: array
          items:
            type: object
            properties:
              departureDate:
                description: Departure date in the format YYYY-MM-DD
                type: string
                example: '2020-02-12'
              departureAirport:
                description: Departure airport code
                maxLength: 3
                type: string
                example: CRA
              destinationAirport:
                description: Destination airport code
                maxLength: 3
                type: string
                example: OTP
              airlineCode:
                description: Airline  code
                maxLength: 2
                minLength: 2
                type: string
                example: TA
              airlineName:
                description: Airline  name
                maxLength: 20
                type: string
                example: Tarom
              serviceClass:
                description: 'Ticket type (class) (economy, business class, etc.)'
                maxLength: 1
                type: string
                example: K
              stopover:
                description: 'Displays the possibility of stop-over for the given ticket; 1 = Stop-over is allowed, 0 - not allowed'
                maxLength: 1
                type: string
                example: 1
              fareCode:
                description: Tariff code
                maxLength: 6
                type: string
                example: 456fgh
              flightNumber:
                description: Flight number
                maxLength: 5
                type: string
                example: 46fgh
            required:
            - departureDate
            - departureAirport
            - destinationAirport
      required:
      - passengerName
      - flightSegments
    ThreeDSecure:
      description: |
        Container for various 3DS parameters.
      type: object
      properties:
        mpiData:
          $ref: '#/components/schemas/MpiData'
        strongCustomerAuthentication:
          $ref: '#/components/schemas/strongCustomerAuthentication'
    MpiData:
      description: |
        Values returned by MPI, after 3DS authentication attempt.
      type: object
      properties:
        eci:
          description: |
            The Electronic Commerce Indicator (ECI) associated with the transaction. This indicator is returned by the card processing networks (Visa, MasterCard, and JCB) to indicate the authentication results of your customer's credit card payment on 3D Secure. Values 0, 1 and 2 are valid for Mastercard cards, while 5, 6 and 7 are valid for Visa cards.
          type: integer
          nullable: true
          enum: [null, 0, 1, 2, 5, 6, 7]
          example: 5
        xid:
          description: |
            The unique identifier for the transaction
          type: string
          example: "75BCD15"
        cavv:
          description: |
            The unique Cardholder Authentication Verification Value (CAVV) associated with the transaction, provided by the card issuer. Base64 encoded.
          type: string
          example: "hmbTh+XZEf/cYwAAAH8kAlcAAAA="
        dsTransactionId:
          description: |
            3DS Dynamic Server transaction ID
          type: string
          example: "1jpe0dc0-i9t2-4067-bcb1-nmt866956sgd"
        version:
          description: |
            3DS version used. If no version is sent, the default is set to 1.
          type: integer
          enum: [1, 2]
          example: 2
    StoredCredentials:
      properties:
        consentType:
          description: |
            Used for the initial transaction in which the customer agrees to using stored card information for subsequent transactions. If consentType is used, useType shouldn't be present. It should have "recurring" value for subsequent scheduled transactions and "onDemand" value for subsequent customer-initiated transactions, or subsequent unscheduled transactions initiated by the merchant.
          enum: ["recurring", "onDemand"]
          type: string
        useType:
          description: |
            Used after consent authorization. It should have "cardholder" value for stored card transactions, initiated by the cardholder, "merchant" value for unscheduled stored card transactions initiated by the merchant and "recurring" for transaction that is part of a series of transactions that use stored card information and that are processed at fixed, regular intervals.
          type: string
          enum: ["cardholder", "merchant", "recurring"]
        useId:
          description: |
            The transaction id in the card scheme system identifying the initial payment in which the customer consented to using stored payment credentials for processing subsequent payments. It should be sent only together with useType.
          type: string
          example: "123456"
    NotificationOptions:
      properties:
        ipnUrl:
          description: |
            The URL where IPN will be sent. If not specified, the IPN URL set on account will be used.
          type: string
          example: "https://notification.payu.com"
          format: uri
    AdditionalDetails:
      type: object
      description: |
        Holds data with additional details for the payment in key/value pairs. <br/> Example: <br/> <b> originalPayuPaymentReference</b>. The value contains the Payu payment reference for the order on which the repayment is attempted. <br/>This node can't contain more than 5 fields.
      additionalProperties:
       type: string
       maxLength: 255
       description: Each key length should be max 50 chars.
    AdditionalDetailsRefund:
      type: object
      description: |
        Holds data with additional details for the refund in key/value pairs. <br/> The value contains the additional details that the merchant wants to keep for that specific refund request. <br/>This node can't contain more than 5 fields and it will be sent back on the refund IPN.
      additionalProperties:
        type: string
        maxLength: 255
        description: Each value length should be max 50 chars.
    AdditionalDetailsIpn:
      type: object
      description: |
        This node sends the data received in refund requests in the `additionalDetails` node. This node will not contain more than 5 fields.
      additionalProperties:
        type: string
        maxLength: 255
        description: Each key length should be max 50 chars.

    strongCustomerAuthentication:
      type: object
      description: Holds data to be passed in a 3D Secure 2.0 redirection flow. <br/><b>Exemptions:</b><br/>Recurring and Merchant Initiated Transactions (MIT).<br/>Only the initial transaction, starting the subscription or recurring cycle will require SCA (3DS 2.0 Authentification). Subsequent transactions will be exempt.<br/><br/>If the transaction is with variable amount and date (such as in case of some utility bills based on usage, like electricity, telecom services etc.), such transaction will be called MIT (Merchant Initiated Transaction) and will be also exempt.<br/><br/>For marking a transaction as a:<br/><ul><li>Merchant initiated transaction (MIT)</li><li>Recurring</li><li>Cardholder initiated transaction (CIT)</li></ul>Please see the dedicated section below of the Stored Credentials documentation. <br/>Of course in the above cases, the merchant must obtain cardholder's consent for charging the card.
      properties:
          cardholder:
            $ref: '#/components/schemas/Cardholder'
          clientEnvironment:
            $ref: '#/components/schemas/ClientEnvironment'
          purchase:
            $ref: '#/components/schemas/Purchase'
          threeDSRequestorPreferences:
            $ref: '#/components/schemas/ThreeDSRequestorPreferences'
      required:
        - clientEnvironment
    Cardholder:
      description: Describes cardholder's account data in merchant's possession, including details of account run for the cardholder in merchant's system.
      type: object
      properties:
        contact:
          $ref: '#/components/schemas/Contact'
        accountInformation:
          type: object
          properties:
            address:
              type: object
              properties:
                match:
                  type: string
                  enum: ["YES", "NO"]
                  description: >
                    Indicates whether the cardholder's shipping address and billing address are the same:
                     * `YES` - Shipping address matches billing address
                     * `NO` - Shipping address does not match billing address
                billing:
                  type: object
                  properties:
                    address3:
                      type: string
                      description: Third line of the street address or equivalent local portion of the cardholder's billing address associated with the card used for this purchase.
                      maxLength: 50
                      example: "445 Mount Eden Road, Mount Eden, Auckland"
                    stateCode:
                      type: string
                      description: The state and province of the cardholder's billing address associated with the card used for this purchase. Should be in ISO 3166-2 format (https://en.wikipedia.org/wiki/ISO_3166-2).
                      minLength: 2
                      maxLength: 6
                      example: "RO-B"
                delivery:
                  type: object
                  properties:
                    address3:
                      type: string
                      description: Third line of the street address or equivalent local portion of the shipping address requested by the cardholder.
                      maxLength: 50
                      example: "445 Mount Eden Road, Mount Eden, Auckland"
                    stateCode:
                      type: string
                      description: The state and province of the shipping address. Should be in ISO 3166-2 format (https://en.wikipedia.org/wiki/ISO_3166-2).
                      minLength: 2
                      maxLength: 6
                      example: "RO-CT"
                    addressFirstUsedDate:
                      type: string
                      description: It is the date when the shipping address used for this transaction was first used with the 3DS Requestor. Should be in ISO_8601 Y-m-d\TH:i:sP format (https://en.wikipedia.org/wiki/ISO_8601).
                      example: '2019-10-02T12:00:14+00:00'
                    addressUsageIndicator:
                      type: string
                      minLength: 2
                      maxLength: 2
                      enum: ["01", "02", "03", "04"]
                      description: >
                        Indicates when the shipping address used for this transaction was first used with the 3DS Requestor.
                         * `01` - This transaction
                         * `02` - Less than 30 days
                         * `03` - 30-60 days
                         * `04` - More than 60 days
            fraudActivity:
              type: string
              enum: ["YES", "NO"]
              description: >
                Indicates whether the merchant experienced suspicious activity on the account:
                 * `YES` - Suspicious activity observed
                 * `NO` - No suspicious activity
            createDate:
              type: string
              description: It is the date when the cardholder opened the account with the 3DS Requestor. Should be in ISO_8601 Y-m-d\TH:i:sP format (https://en.wikipedia.org/wiki/ISO_8601).
              example: '2019-10-02T12:00:14+00:00'
            pastOrdersYear:
              anyOf:
                - type: number
                - type: string
                  minLength: 1
                  maxLength: 3
              description: Number of transactions (successful and abandoned) for this cardholder account with the 3DS Requestor across all payment accounts in the previous year.
              example: 324
            pastOrdersDay:
              anyOf:
                - type: number
                - type: string
                  minLength: 1
                  maxLength: 3
              description: Number of transactions (successful and abandoned) for this cardholder account with the 3DS Requestor across all payment accounts in the previous 24hours.
              example: 27
            purchasesLastSixMonths:
              anyOf:
                - type: number
                - type: string
                  minLength: 1
                  maxLength: 4
              description: Number of purchases with this cardholder account during the previous six months.
              example: 12
            changeDate:
              type: string
              description: It is the date when the cardholder’s account with the 3DS Requestor was last changed, including billing or shipping address, new payment account, or new user(s) added. Should be in ISO_8601 Y-m-d\TH:i:sP format (https://en.wikipedia.org/wiki/ISO_8601).
              example: '2019-10-02T12:00:14+00:00'
            changeIndicator:
              type: string
              minLength: 2
              maxLength: 2
              enum: ["01", "02", "03", "04"]
              description: >
                Length of time since the cardholder’s account information with the 3DS Requestor was last changed, including billing or shipping address, new payment account, or new user(s) added.
                 * `01` - During this transaction
                 * `02` - Less than 30 days
                 * `03` - 30-60 days
                 * `04` - More than 60 days
            ageIndicator:
              type: string
              minLength: 2
              maxLength: 2
              enum: ["01", "02", "03", "04", "05"]
              description: >
                Length of time that the cardholder has had the account with the 3DS Requestor.
                 * `01` - No account
                 * `02` - Created this transaction
                 * `03` - Less than 30 days
                 * `04` - 30-60 days
                 * `05` - More than 60 days
            passwordChangedDate:
              type: string
              description: It is the date when cardholder’s account with the 3DS Requestor had a password change or account reset. Should be in ISO_8601 Y-m-d\TH:i:sP format (https://en.wikipedia.org/wiki/ISO_8601).
              example: '2019-10-02T12:00:14+00:00'
            passwordChangeIndicator:
              type: string
              minLength: 2
              maxLength: 2
              enum: ["01", "02", "03", "04", "05"]
              description: >
                Indicates the length of time since the cardholder’s account with the 3DS Requestor had a password change or account reset.
                 * `01` - No change
                 * `02` - Changed this transaction
                 * `03` - Less than 30 days
                 * `04` - 30-60 days
                 * `05` - More than 60 days
            nameToRecipientMatch:
              type: string
              enum: ["YES", "NO"]
              description: >
                Indicates if the cardholder name on the account is identical to the shipping name used for this transaction.
                 * `YES` - Account name identical to shipping name
                 * `NO` - Account name different from shipping name
            addCardAttemptsDay:
              anyOf:
                - type: number
                - type: string
              description: Indicates the number of attempts to add a card to cardholder's account in merchant's system within last 24 hours.
              maxLength: 3
              example: 12
            authMethod:
              type: string
              maxLength: 2
              minLength: 2
              enum: ["01", "02", "03", "04", "05", "06"]
              description: >
                The mechanism used by the cardholder to authenticate to the 3DS Requestor.
                 * `01` - No authentication occurred (e.g. Guest Checkout)
                 * `02` - Login to the cardholder account at the merchant system using merchant system credentials
                 * `03` - Login to the cardholder account at the merchant system using a Federated ID
                 * `04` - Login to the cardholder account at the merchant system using Issuer credentials
                 * `05` - Login to the cardholder account at the merchant system using third-party authentication
                 * `06` - Login to the cardholder account at the merchant system using FIDO Authenticator
            authDateTime:
              type: string
              description: Date and time of the cardholder authentication (in UTC). Should be in ISO_8601 Y-m-d\TH:i:sP format (https://en.wikipedia.org/wiki/ISO_8601).
              example: '2019-10-02T12:00:14+00:00'
            requestorAuthenticationData:
              type: string
              description: Information about how the 3DS Requestor authenticated the cardholder before or during the transaction.
            additionalDetails:
              type: string
              description: Additional information about the cardholder’s account provided by the 3DS Requestor.
              example: "Additional details here"
            cardAddedIndicator:
              type: string
              maxLength: 2
              minLength: 2
              enum: ["01", "02", "03", "04", "05"]
              description: >
                Indicates if and when the card was stored in the merchant account.
                 * `01` - No account (guest checkout)
                 * `02` - During this transaction
                 * `03` - Less than 30 days
                 * `04` - 30-60 days
                 * `05` -  More than 60 days
            cardAddedDate:
              type: string
              description: Date when card has been stored in the merchant account. Should be in ISO_8601 Y-m-d\TH:i:sP format (https://en.wikipedia.org/wiki/ISO_8601).
              example: '2019-10-02T12:00:14+00:00'
    ClientEnvironment:
      type: object
      properties:
        deviceChannel:
          type: string
          enum: ["01", "02", "03"]
          description: >
            Indicates the type of channel interface being used to initiate the transaction.
             * `01` - The transaction was initiated through the mobile SDK.
             * `02` - The transaction was initiated through a web browser.
             * `03` - 3DS Requestor Initiated. The 3DS Requestor Initiated device channel allows 3-D Secure authentication without the presence of the cardholder.
        browser:
          type: object
          description: If some properties are not present, we will replace them with our default values
          properties:
            acceptHeader:
              type: string
              description: Exact content of the HTTP accept headers as sent to the 3DS Requestor from the cardholder’s browser.
              maxLength: 2048
              example: "text/html"
              default: '*/*'
            requestIp:
              type: string
              description: IP address of the browser as returned by the HTTP headers to the 3DS Requestor.
              maxLength: 45
              example: "127.0.0.1"
            javaEnabled:
              type: string
              enum: ["YES", "NO"]
              description: >
                It represents the ability of the cardholder's browser to execute Java.
                 * `YES` - Cardholder's browser can execute Java
                 * `NO` - Cardholder's browser can't execute Java
            language:
              type: string
              description: It represents the browser language as defined in IETF BCP47 (https://en.wikipedia.org/wiki/IETF_language_tag).
              minLength: 1
              maxLength: 8
              example: "en-US"
            colorDepth:
              anyOf:
                - type: number
                  enum: [1, 4, 8, 15, 16, 24, 32, 48]
                - type: string
                  enum: ["1", "4", "8", "15", "16", "24", "32", "48"]
              description: >
                The bit depth of the color palette for displaying images, in bits per pixel.
              example: 24
              default: 24
            screenHeight:
              anyOf:
                - type: number
                - type: string
                  maxLength: 6
                  minLength: 1
              description: The total height of the cardholder's screen, in pixels.
              example: 864
              default: 1080
            screenWidth:
              anyOf:
                - type: number
                - type: string
                  maxLength: 6
                  minLength: 1
              description: The total width of the cardholder's screen, in pixels.
              example: 1536
              default: 1920
            timezone:
              anyOf:
                - type: number
                - type: string
                  maxLength: 5
                  minLength: 1
              description: The time difference between UTC time and the cardholder's browser local time, in minutes.
              example: 300
              default: -180
            userAgent:
              type: string
              description: Exact content of the HTTP user-agent header.
              maxLength: 2048
              example: "Mozilla/5.0"
              default: "Mozilla/5.0"
    Contact:
      type: object
      properties:
        phone:
          type: object
          properties:
            home:
              type: object
              properties:
                countryPrefix:
                  type: string
                  description: The country code of the home phone number. Refer to ITU-E.164 (https://en.wikipedia.org/wiki/E.164) for additional information on format.
                  maxLength: 3
                  example: "40"
                subscriber:
                  type: string
                  description: The cardholder's home phone number (without the country code). Refer to ITU-E.164 (https://en.wikipedia.org/wiki/E.164) for additional information on format.
                  maxLength: 15
                  example: "5417543010"
            mobile:
              type: object
              properties:
                countryPrefix:
                  type: string
                  description: The country code of the mobile phone number. Refer to ITU-E.164 (https://en.wikipedia.org/wiki/E.164) for additional information on format.
                  maxLength: 3
                  example: "40"
                subscriber:
                  type: string
                  description: The cardholder's mobile phone number (without the country code). Refer to ITU-E.164 (https://en.wikipedia.org/wiki/E.164) for additional information on format.
                  maxLength: 15
                  example: "5231543010"
            work:
              type: object
              properties:
                countryPrefix:
                  type: string
                  description: The country code of the work phone number. Refer to ITU-E.164 (https://en.wikipedia.org/wiki/E.164) for additional information on format.
                  maxLength: 3
                  example: "40"
                subscriber:
                  type: string
                  description: The cardholder's work phone number (without the country code). Refer to ITU-E.164 (https://en.wikipedia.org/wiki/E.164) for additional information on format.
                  maxLength: 15
                  example: "0031543010"
    Recurring:
      type: object
      properties:
        frequencyDays:
          type: number
          description: Indicates the minimum number of days between authorizations.
          maxLength: 4
          example: 10
        expiryDate:
          type: number
          description: It is the date after which no further authorizations shall be performed. Should be in ISO_8601 Y-m-d\TH:i:sP format (https://en.wikipedia.org/wiki/ISO_8601).
          example: '2019-10-02T12:00:14+00:00'
    Purchase:
      type: object
      properties:
        recurring:
          $ref: '#/components/schemas/Recurring'
        transactionType:
          type: string
          minLength: 2
          maxLength: 2
          enum: ["01", "10", "11", "28"]
          description: >
            Identifies the type of transaction being authenticated.
             * `01` - Goods/ Service Purchase
             * `10` - Account Funding
             * `11` - Quasi-Cash Transaction
             * `28` - Prepaid Activation and Load
        shipIndicator:
          type: string
          minLength: 2
          maxLength: 2
          enum: ["01", "02", "03", "04", "05", "06", "07"]
          description: >
            The shipping method selected by the customer.
             * `01` - Ship to cardholder billing address
             * `02` - Ship to another verified address on file with merchant
             * `03` - Ship to address that is different than billing address
             * `04` - Ship to store (store address should be populated on request)
             * `05` - Digital goods
             * `06` - Travel and event tickets, not shipped
             * `07` - Other
        preOrderIndicator:
          type: string
          minLength: 2
          maxLength: 2
          enum: ["01", "02"]
          description: >
            Indicates whether cardholder is placing an order for merchandise with a future availability or release date.
             * `01` - Merchandise available
             * `02` - Future availability
        preOrderDate:
          type: string
          description: Expected date that a pre-ordered purchase will be available. Should be in ISO_8601 Y-m-d\TH:i:sP format (https://en.wikipedia.org/wiki/ISO_8601).
          example: '2019-10-02T12:00:14+00:00'
        deliveryTimeFrame:
          type: string
          minLength: 2
          maxLength: 2
          enum: ["01", "02", "03", "04"]
          description: >
            Indicates the merchandise delivery time frame.
             * `01` - Electronic delivery
             * `02` - Same day shipping
             * `03` - Overnight shipping
             * `04` - Two or more days shipping
        reorderedIndicator:
          type: string
          minLength: 2
          maxLength: 2
          enum: ["01", "02"]
          description: >
            Indicates whether the cardholder is reordering previously purchased merchandise.
             * `01` - First time ordered
             * `02` - Reordered
        merchantFunds:
           type: object
           properties:
             amount:
               type: number
               maxLength: 15
               description: For prepaid or gift card purchase, the purchase amount total of prepaid or gift card(s) in major units.
               example: 1293
             currency:
               minLength: 3
               maxLength: 3
               type: string
               description: For prepaid or gift card purchase, ISO 4217 three-digit currency code of the gift card.
               example: "RON"
    ThreeDSRequestorPreferences:
      type: object
      properties:
        challenge:
          type: object
          properties:
            indicator:
              type: string
              enum: ["01", "02", "03"]
              description: >
                Indicates whether a challenge is requested for this transaction. For example, for Payment Authentication, a 3DS Requestor may have concerns about the transaction, and request a challenge.
                 * `01` - No challenge requested
                 * `02` - Challenge requested (3DS Requestor Preference)
                 * `03` - Challenge requested (Mandate)
              maxLength: 2
              minLength: 2
            ui:
              type: object
              properties:
                windowSize:
                  type: string
                  enum: ["01", "02", "03", "04", "05"]
                  description: >
                    An override field that you can pass in to set the challenge window size to display to the end cardholder. The Access Control Server (ACS) will reply with content that is formatted appropriately to this window size to allow for the best user experience. The sizes are width x height in pixels of the window displayed in the cardholder browser window.
                     * `01` - 250x400
                     * `02` - 390x400
                     * `03` - 500x600
                     * `04` - 600x400
                     * `05` - Full page
                  minLength: 2
                  maxLength: 2
    Fx:
      type: object
      properties:
        currency:
          $ref: '#/components/schemas/Currency'
        exchangeRate:
          anyOf:
            - type: number
              format: double
            - type: string
          example: "0.2132"
      required:
      - currency
      - exchangeRate
    PaymentPageOptions:
      description: These options are used only if usePaymentPage is set on 'YES'
      type: object
      properties:
        orderTimeout:
          description: The time in seconds after which the order will expire
          type: number
          format: integer
          example: 3600
    ApplePayToken:
      description: |
        Required if the payment method is an online one and no merchantToken or cardDetails are sent. This is the object received from Apple.
        Url-encoded ApplePay payments token must be send (the value of `paymentData` node. ex: `{version:"", signature:"", header:"", data:""})`.
        More details about Apple Pay Token [here](/docs/apple-pay/)
      type: object
      properties:
        data:
          type: string
        header:
          type: object
          properties:
            applicationData:
              type: string
            ephemeralPublicKey:
              type: string
            publicKeyHash:
              type: string
            transactionId:
              type: string
          required:
          - applicationData
          - ephemeralPublicKey
          - publicKeyHash
          - transactionId
        signature:
          type: string
        version:
          type: string
      required:
      - data
      - header
      - signature
      - version
    GooglePayToken:
      description: |
        URL-encoded Google Pay token (the JSON value representation of the [`paymentData`](https://developers.google.com/pay/api/android/guides/resources/payment-data-cryptography?hl=en#payment-method-token-structure) node).<br/>
        To begin your Web integration with Google Pay, please check the [Google Pay Web developer documentation](https://developers.google.com/pay/api/web/overview).

        Ensure that your integration follows the items described in [Google Pay Web integration checklist](https://developers.google.com/pay/api/web/overview),
        and also the [Google Pay Web Brand Guidelines](https://developers.google.com/pay/api/web/guides/brand-guidelines).

        Additionally, you must adhere to the [Google Pay APIs Acceptable Use Policy](https://payments.developers.google.com/terms/aup) and accept the terms defined in the
        [Google Pay API Terms of Service](https://payments.developers.google.com/terms/sellertos).

        The `gateway` parameter from the [`TokenizationSpecification`](https://developers.google.com/pay/api/android/reference/request-objects?hl=en#PaymentMethodTokenizationSpecification)
        should have the following value, depending on the platform you are using (see the below snippet):

        * `payuro` - for PayU Romania

        ```json
        const tokenizationSpecification = {
            type: 'PAYMENT_GATEWAY',
            parameters: {
                'gateway': '[the platform code]',
                'gatewayMerchantId': '[your merchant code]'
            }
        };
        ```

        The value of the `gatewayMerchantId` parameter should be your merchant code.

        You should have a similar configuration for your [`PaymentMethod`](https://developers.google.com/pay/api/android/reference/request-objects?hl=en#PaymentMethod) node as below.
        The values of these items are configured on PayU's side as well. Please contact us to ensure you have the proper setup for your account.

        ```json
        const allowedCardNetworks = ['MASTERCARD', 'VISA'];
        const allowedCardAuthMethods = [
          'PAN_ONLY', 'CRYPTOGRAM_3DS'
        ];
        ```

        In certain cases, 3DS may be requested for Google Pay payments as well. Please ensure that your implementation is ready to support such transactions.
        Check the `url` parameter from this endpoint response.
      type: string
    MerchantToken:
      description: Required if the payment method is an online one and no digital payment method (networkToken) or cardDetails are sent
      type: object
      properties:
        tokenHash:
          type: string
          example: d41d8cd98f00b204e9800998ecf8427e
        cvv:
          $ref: '#/components/schemas/CardCvv'
        owner:
          $ref: '#/components/schemas/CardOwner'
      required:
      - tokenHash

    OneTimeUseToken:
      description: Required if the payment method is an online one and want to use one time use token (see `Secure Fields` documentation).
      type: object
      properties:
        token:
          type: string
          description: The token can only be used in Secure Fields call and in the Authorization call.
          example: QyMdbnU0iStRpE0ZG5islpPPnUN7NpWTUOqvFzpWydlnWYZp62b+yJmoxxZOSnZ0lOf0ajj7c6tHi8bLRaLk/Q==
        sessionId:
          description: This is an unique identifier for the session. This must be the same sessionId used when the token was created. This must be unique per successful authorization.
          type: string
          example: 692da2c6-8c18-4ca0-a515-8c293c7c8305
      required:
        - token
        - sessionId
    CreditDetails:
      description: These are the parameters that have to be sent when a credit is requested. This flow has to be previously activated for the merchant and works only with one of CREDIT_SLICE or CREDIT_BUY_NOW_PAY_LATER payment methods.
      type: object
      properties:
        limits:
          type: array
          minItems: 1
          maxItems: 1
          description: Limits for credit request
          items:
            $ref: '#/components/schemas/CreditLimit'
        customerUUID:
          description: This is an unique identifier of the customer. The same value has to be sent in all credit calls for a specific merchant (value should be uuid v4 format).
          type: string
          example: 692da2c6-8c18-4ca0-a515-8c293c7c8305
        customerMasterUUID:
          description: This is an unique identifier of the customer. The same value has to be sent in all credit calls for a specific merchant (value should be uuid v4 format).
          type: string
          example: ff851d4a-0ec8-47ab-912e-a80963e5cb4a
        scoring:
          type: number
          format: float
          example: 0.4
          description: This is the risk level for the credit.
        cnp:
          description: This is the CNP of the customer that wants the credit.
          type: string
          example: '1234956784245'
        sourceOfIncome:
          type: string
          example: Salaries
          description: This is the source of income from which the credit will be paid.
        uncensoredScoring:
          type: number
          format: float
          example: 0.5
          description: This is a credit uncensored score and it is used in Risk Matrix.
        nrInstalments:
          anyOf:
            - type: integer
            - type: string
          example: 2
          description: This is the number of installments that a SLICE order can be divided into.
        nrDaysDueDate:
          type: integer
          example: 22
          description: This is the number of calendar days allowed between the moment an order is placed and the due date for repayment.
        financialPartner:
          type: string
          example: "PARTNER"
          description: This is the value for the financial partner.
        campaignCode:
          type: string
          example: "CAMPAIGN01"
          description: This is the value for the campaign code.
        paymentMethodLimitAmount:
          type: integer
          example: 2000
          description: Amount limit for the credit when credit type is BNPL Exposure.
        lendingAdditionalDetails:
          type: object
          maxProperties: 30
          description: This node holds information that is agreed upon the merchant and the lending provider in key/value pairs. It can contain a maximum of 30 properties.
          additionalProperties:
            type: string
            maxLength: 200
            description: Each key must be a string value with a maximum length of 50 chars.
      required:
        - limits
        - customerUUID
        - customerMasterUUID
        - scoring

    CardDetails:
      description: Required if the payment method is an online one and no digital payment method (networkToken) or merchantToken are sent
      type: object
      properties:
        number:
          description: The card number on which the payment authorization will be made.
          type: string
          minLength: 8
          maxLength: 19
          example: 5181510361644410
        expiryMonth:
          description: The month in which the card used expires
          anyOf:
            - type: integer
            - type: string
          minimum: 1
          maximum: 12
          example: 12
        expiryYear:
          description: The year in which the card used expires
          anyOf:
            - type: integer
            - type: string
          maximum: 9999
          example: 2024
        cvv:
          $ref: '#/components/schemas/CardCvv'
        owner:
          $ref: '#/components/schemas/CardOwner'
        timeSpentTypingNumber:
          type: integer
          example: 30
          description: Time in seconds spent by user to insert card number
        timeSpentTypingOwner:
          type: integer
          example: 12
          description: Time in seconds spent by user to insert card owner
      required:
      - number
      - expiryMonth
      - expiryYear
    RefundRequest:
      type: object
      properties:
        payuPaymentReference:
          $ref: '#/components/schemas/PayuPaymentReference'
        originalAmount:
          description: Original amount of the transaction (including installments cost if applicable)
          anyOf:
            - type: number
            - type: string
          format: double
          example: 5.66
        currency:
          $ref: '#/components/schemas/Currency'
        amount:
          description: Amount that will be refunded to client.
            Must not exceed difference between originalAmount and previous refund requests.
            Amount should be a strict positive number.
            If the merchant is a [marketplace account](#section/Overview/Marketplace-payment-flow) and if this amount is smaller than originalAmount, the `products` key must be also sent.
          anyOf:
            - type: number
            - type: string
          format: double
          example: 5.66
        merchantRefundReference:
          description: Refund reference value that could be filled with an identifier for the request.
          type: string
          format: string
          example: 6c6ATzmtUD
        loyalty:
          type: array
          items:
            type: object
            properties:
              amount:
                type: number
                format: integer
                example: 300
              type:
                type: string
                format: string
                enum: ['bns', 'fbb']
        installmentsAmount:
          description: Installments fee amount to be returned to client.
            Must not exceed difference between initial installments fee amount and previous refund requests.
          type: number
          format: double
          example: 5.66
          nullable: true
        products:
          type: array
          nullable: true
          items:
            type: object
            properties:
              sku:
                description: Sku of original product. For refund per products is mandatory.
                anyOf:
                  - type: string
                  - type: number
              amount:
                description: Amount of the original product that will be refunded. It must not exceed (unitPrice * quantity) of the original product.
                type: number
                format: double
                example: 4.6
              marketplace:
                $ref: '#/components/schemas/Marketplace'
            required:
            - sku
            - amount
        useFastRefund:
          type: string
          description:
            Value "yes" means the Fast Refund feature will be used if the merchant and the order terminal support this feature, otherwise an error message will be returned.
            Value "try" is similar to value "yes" only that it will not return the error. In case the merchant and/or the terminal do not support Fast Refund, the IRN will be silently registered as a regular refund request.
            Value "no" is also the default when this parameter is not sent. It will register the IRN as a regular refund request, no matter what settings for Fast Refund exist on the merchant and terminal.
          enum:
            - 'yes'
            - 'try'
            - 'no'
          default: 'no'
        marketplaceV1:
          description:
            Mandatory for payment using marketplaceV1 version <i>(deprecated)</i><br/>
            <b>marketplaceV1</b> and <b>products</b> nodes can't be sent together
          type: array
          items:
            properties:
              merchant:
                type: string
                example: PAYU_2
                description: Merchant identifier in PayU system
              amount:
                description: Amount to be refunded to the specific merchant.
                type: number
                format: double
                example: 4.6
            required:
              - merchant
              - amount
          deprecated: true
        additionalDetails:
          $ref: '#/components/schemas/AdditionalDetailsRefund'

      required:
      - payuPaymentReference
      - originalAmount
      - currency
      - amount

    CaptureRequest:
      type: object
      properties:
        payuPaymentReference:
          $ref: '#/components/schemas/PayuPaymentReference'
        originalAmount:
          anyOf:
            - type: number
            - type: string
          format: double
          example: 5.66
        amount:
          description: Amount that will be captured (including installmentsAmount and sum of all products)
          anyOf:
            - type: number
            - type: string
          format: double
          example: 5.66
        currency:
          $ref: '#/components/schemas/Currency'
        installmentsAmount:
          description: The amount of installments fee to be captured. Only works for marketplace orders.
          anyOf:
            - type: number
            - type: string
          format: double
          example: 5.66
        products:
          type: array
          nullable: true
          items:
            type: object
            properties:
              sku:
                description: Sku of original product. For capture per products is mandatory. Only works for marketplace orders.
                anyOf:
                  - type: number
                  - type: string
              amount:
                description: Amount of the original product that will be captured. It must not exceed (unitPrice * quantity) of the original product.
                type: number
                format: double
                example: 4.6
              marketplace:
                $ref: '#/components/schemas/MarketplaceCaptureObject'
            required:
            - sku
            - amount
      required:
        - payuPaymentReference
        - originalAmount
        - currency
    PayoutChannel:
      type: object
      properties:
        name:
          description: "Description of payout channel."
          type: string
          example: EUR channel
        iban:
          description: "IBAN when to do seller payouts. Must be a valid IBAN, if not payouts will not be done. No space are allowed."
          format: iban
          minLength: 15
          maxLength: 32
          example: TR330006100519786457841326
        currency:
          type: string
          format: ISO_CODE
          minLength: 3
          example: EUR
        bank:
          type: object
          properties:
            bic:
              type: string
              format: SWIFT_CODE
              minLength: 3
              maxLength: 100
              example: SBIN IN BB 455
            name:
              type: string
              format: Bank name
              minLength: 3
              maxLength: 100
              example: Transilvania Bank
        ruleId:
          type: string
          minLength: 36
          maxLength: 36
          example: 7cff8d290e58-b4de-4c31-ac82-ac1ae54c

    MarketplaceSellerId:
      description: "Id of marketplace seller generated by PayU"
      format: uuid
      example: 49a88d24-7615-11e8-adc0-fa7ae01bbebc

    MarketplaceSellerName:
      description: "Seller name"
      type: string
      maxLength: 255

    MarketplaceSellerEmail:
      description: "Seller email"
      type: string
      maxLength: 255
      example: office@test.com

    MarketplaceSellerTaxId:
      description: "Tax id of marketplace seller"
      type: string
      maxLength: 255
      example: 234tr32

    MarketplaceSellerDebitItems:
      type: object
      properties:
        sellerId:
          format: uuid
          example: "49a88d24-7615-41e8-adc0-fa7ae01bbebu"
        currency:
          type: string
          format: ISO_CODE
          minLength: 3
          example: EUR
        amount:
          anyOf:
            - type: number
            - type: string
          format: double
          example: 352.30
          description: "Debit from seller"

    MarketplaceSellerCreditItems:
      type: object
      properties:
        sellerId:
          format: uuid
          example: "49a88d24-7615-41e8-adc0-fa7ae01bbebu"
        currency:
          type: string
          format: ISO_CODE
          minLength: 3
          example: EUR
        amount:
          anyOf:
            - type: number
            - type: string
          format: double
          example: 352.30
          description: "Credit seller"


    MarketplaceSellerKyc:
      description: "Optional. If KYC was not done, it does not need to be sent"
      properties:
        timestamp:
          description: "Date time when seller accept marketplace agreement.Must be in ISO_8601 format (https://en.wikipedia.org/wiki/ISO_8601)"
          type: string
          format:  ISO_8601 datetime
          example: '2018-08-02T12:00:14+00:00'
        ip:
          type: string
          format: ip
          example: 192.168.1.1
      required:
      - timestamp
      - ip

    MarketplaceSellerDate:
        description: "UTC Date time when seller was created. Must be in ISO_8601 format (https://en.wikipedia.org/wiki/ISO_8601)"
        type: string
        format:  ISO_8601 datetime
        example: '2018-08-02T12:00:14+00:00'


    MarketplaceSellerTransferTo:
      description: "Seller that receive money"
      format: uuid
      example: 49a88d24-7615-41e8-adc0-fa7ae01bbebu

    MarketplaceSellerTransferFrom:
      description: "Seller that send money"
      format: uuid
      example: 49a88d24-7615-11e8-adc0-fa7ae01bbebc

    MarketplaceSellerTransferDescription:
      description: "Details of transfer"
      type: string
      maxLength: 255
      example: "Description of transfer"

    MarketplaceSellerTransferAmount:
      description: "Amount of transfer"
      anyOf:
        - type: number
        - type: string
      format: double
      example: "10.50"

    MarketplaceSellerTransferCurrency:
      description: "The currency used for transfer"
      type: string
      minLength: 3
      example: "EUR"

    SellersResponse:
      type: object
      properties:
        id:
          type: string
          minLength: 36
          maxLength: 36
          example: 7cff8d290e58-b4de-4c31-ac82-ac1ae54c
        name:
          type: string
          minLength: 3
          maxLength: 255
          example: Test merchant
        email:
          type: string
          format: email
          minLength: 5
          maxLength: 255
          example: office@test.com
        taxId:
          type: string
          minLength: 3
          maxLength: 255
          example: '123456'
        payoutChannels:
          type: array
          items:
              type: object
              properties:
                iban:
                  type: string
                  format: iban
                  minLength: 15
                  maxLength: 32
                  example: TR330006100519786457841326
                currency:
                  type: string
                  format: ISO_CODE
                  minLength: 3
                  example: EUR
                ruleId:
                  type: string
                  minLength: 36
                  maxLength: 36
                  example: 7cff8d290e58-b4de-4c31-ac82-ac1ae54c
        kyc:
          type: object
          nullable: true
          properties:
            timestamp:
              type: string
              nullable: true
              format: ISO_8601 datetime
              description: "Date time when seller accept marketplace agreement. Must be in ISO_8601 format (https://en.wikipedia.org/wiki/ISO_8601)"
              example: '2018-08-02T12:00:14+00:00'
            ip:
              type: string
              nullable: true
              format: ip
              example: 192.168.1.1
        date:
              type: string
              format: ISO_8601 datetime
              description: "UTC date time when seller was created in ISO 8601 format. Must be in ISO_8601 format (https://en.wikipedia.org/wiki/ISO_8601)"
              example: '2018-08-02T12:00:14+00:00'

    MarketplaceSellerRequest:
      type: object
      properties:
        name:
          $ref: '#/components/schemas/MarketplaceSellerName'
        email:
          $ref: '#/components/schemas/MarketplaceSellerEmail'
        taxId:
          $ref: '#/components/schemas/MarketplaceSellerTaxId'
        payoutChannels:
          type: array
          items:
            $ref: '#/components/schemas/PayoutChannel'
        kyc:
          $ref: '#/components/schemas/MarketplaceSellerKyc'
      required:
      - name
      - email
      - taxId
      - payoutChannels


    MarketplaceSellerTransferRequest:
      type: object
      properties:
        description:
          $ref: '#/components/schemas/MarketplaceSellerTransferDescription'
        amount:
          $ref: '#/components/schemas/MarketplaceSellerTransferAmount'
        currency:
          $ref: '#/components/schemas/MarketplaceSellerTransferCurrency'
        from:
          $ref: '#/components/schemas/MarketplaceSellerTransferFrom'
        to:
          $ref: '#/components/schemas/MarketplaceSellerTransferTo'

    MarketplaceSellerTransferResponse:
      type: object
      properties:
        description:
          $ref: '#/components/schemas/MarketplaceSellerTransferDescription'
        amount:
          $ref: '#/components/schemas/MarketplaceSellerTransferAmount'
        currency:
          $ref: '#/components/schemas/MarketplaceSellerTransferCurrency'
        from:
          $ref: '#/components/schemas/MarketplaceSellerTransferFrom'
        to:
          $ref: '#/components/schemas/MarketplaceSellerTransferTo'
        code:
          type: number
          enum:
            - 200
        message:
          type: string
          enum:
            - Success

    MarketplaceSellerDebitResponse:
      type: object
      properties:
        description:
          $ref: '#/components/schemas/MarketplaceSellerTransferDescription'
        items:
          type: array
          items:
            $ref: '#/components/schemas/MarketplaceSellerDebitItems'
        code:
          type: number
          enum:
            - 200
        message:
          type: string
          enum:
            - Success

    MarketplaceSellerCreditResponse:
      type: object
      properties:
        description:
          $ref: '#/components/schemas/MarketplaceSellerTransferDescription'
        items:
          type: array
          items:
            $ref: '#/components/schemas/MarketplaceSellerCreditItems'
        code:
          type: number
          enum:
            - 200
        message:
          type: string
          enum:
            - Success

    MarketplaceSellerDebitRequest:
      type: object
      properties:
        description:
          $ref: '#/components/schemas/MarketplaceSellerTransferDescription'
        items:
          type: array
          items:
            $ref: '#/components/schemas/MarketplaceSellerDebitItems'

    MarketplaceSellerCreditRequest:
      type: object
      properties:
        description:
          $ref: '#/components/schemas/MarketplaceSellerTransferDescription'
        items:
          type: array
          items:
            $ref: '#/components/schemas/MarketplaceSellerCreditItems'

    MarketplacePayoutRulesResponse:
      type: object
      properties:
        items:
          description: List of existing payout rules
          type: array
          items:
            $ref: '#/components/schemas/PayoutRule'
        code:
          $ref: '#/components/schemas/2xxResponseCode'
        message:
          $ref: '#/components/schemas/ResponseMessage'

    PayoutRule:
      type: object
      properties:
        ruleId:
          type: string
          minLength: 36
          maxLength: 36
          example: 7cff8d290e58-b4de-4c31-ac82-ac1ae54c
        description:
          type: string
          minLength: 3
          maxLength: 255
          example: Run every thursday

    MarketplaceSellerResponse:
      type: object
      properties:
        code:
          $ref: '#/components/schemas/2xxResponseCode'
        message:
          $ref: '#/components/schemas/ResponseMessage'
        id:
          $ref: '#/components/schemas/MarketplaceSellerId'
        name:
          $ref: '#/components/schemas/MarketplaceSellerName'
        email:
          $ref: '#/components/schemas/MarketplaceSellerEmail'
        taxId:
          $ref: '#/components/schemas/MarketplaceSellerTaxId'
        payoutChannels:
          type: array
          items:
            $ref: '#/components/schemas/PayoutChannel'
        kyc:
          $ref: '#/components/schemas/MarketplaceSellerKyc'
        date:
          $ref: '#/components/schemas/MarketplaceSellerDate'

    MarketplaceSellerResponseNotification:
      type: object
      properties:
        id:
          $ref: '#/components/schemas/MarketplaceSellerId'
        name:
          $ref: '#/components/schemas/MarketplaceSellerName'
        email:
          $ref: '#/components/schemas/MarketplaceSellerEmail'
        taxId:
          $ref: '#/components/schemas/MarketplaceSellerTaxId'
        payoutChannels:
          type: array
          items:
            $ref: '#/components/schemas/PayoutChannel'
        kyc:
          $ref: '#/components/schemas/MarketplaceSellerKyc'
        date:
          $ref: '#/components/schemas/MarketplaceSellerDate'

    MarketplaceSellersResponse:
      type: object
      properties:
        totalItems:
          type: integer
          example: 678
          description: Total number of results
        pageSize:
          type: string
          example: 1000
          description: Number of results to be returned
        page:
          type: string
          example: 1
          description: Number of page
        items:
          description: List of sellers from the selected page
          type: array
          items:
              $ref: '#/components/schemas/SellersResponse'
        code:
          $ref: '#/components/schemas/2xxResponseCode'
        message:
          $ref: '#/components/schemas/ResponseMessage'

    IpnRequest:
      type: object
      properties:
        orderData:
          $ref: '#/components/schemas/IpnOrderData'
        paymentResult:
          $ref: '#/components/schemas/IpnPaymentResult'
        client:
          $ref: '#/components/schemas/IpnClientData'
        products:
          $ref: '#/components/schemas/IpnProducts'
        dateTime:
          type: string
          example: '20190114143730'
          description: Date time value for the moment of the sending of the request in 'YYYYMMDDHHMMSS' format
        authorization:
          $ref: '#/components/schemas/AuthorizationResource'
        refund:
            $ref: '#/components/schemas/RefundResource'
        capture:
            $ref: '#/components/schemas/CaptureResource'
        additionalDetails:
          $ref: '#/components/schemas/AdditionalDetailsIpn'

    MerchantTokenNotification:
      type: object
      properties:
        token:
          type: string
          example: 'd41d8cd98f00b204e9800998ecf8427e'
          description: 'Token string generated previously by using the Create Token endpoint of Token API'
        originalTransaction:
          type: object
          description: |
            Identifiers of the original transaction that generated the token.
            This is an optional node. As we develop new APIs for tokenization, cards could get tokenized without being attached to any transaction in our system.
          properties:
            payuPaymentReference:
              type: integer
              description: 'Unique numeric identifier generated by PayU upon creating an authorization by using the Payment API.'
              example: 123456
            merchantPaymentReference:
              type: string
              description: 'Identifier established by the merchant, sent on the request body used to create an authorization by using the Payment API.'
              example: '987654'

    TokenSuccessResponse:
      allOf:
      - type: object
        properties:
          code:
            $ref: '#/components/schemas/2xxResponseCode'
          message:
            $ref: '#/components/schemas/ResponseMessage'
          status:
            $ref: '#/components/schemas/SuccessResponseStatus'
        required:
          - code
          - message
          - status
      - $ref: '#/components/schemas/TokenDetails'

    GetTokenSuccessResponse:
      allOf:
      - type: object
        properties:
          code:
            $ref: '#/components/schemas/2xxResponseCode'
          message:
            $ref: '#/components/schemas/ResponseMessage'
          status:
            $ref: '#/components/schemas/SuccessResponseStatus'
        required:
          - code
          - message
          - status
      - $ref: '#/components/schemas/GetTokenDetails'

    TokenDetails:
      type: object
      properties:
        token:
          type: string
          description: 'Token string generated for the given order (refNo)'
          example: 'd41d8cd98f00b204e9800998ecf8427e'
        cardUniqueIdentifier:
          description: 'Card unique identifier'
          type: string
          example: 'e9fc5107db302fa8373efbedf55a1614b5a3125ee59fe274e7dc802930d68f6d'
        expirationDate:
          type: string
          description: It is the date when the token expires. Should be in ISO_8601 YYYY-MM-DD format (https://en.wikipedia.org/wiki/ISO_8601).
          format: date
          example: '2023-06-10'
        cardHolderName:
          description: 'The card holder name'
          type: string
          example: 'Test'
        tokenStatus:
          description: 'The token status'
          type: string
          enum: [ 'ACTIVE', 'EXPIRED', 'CANCELED' ]
        lastFourDigits:
          type: string
          example: "1111"
          description: Last four digits of the requested card
        cardExpirationDate:
          type: string
          example: "2023-08-31"
          description: Expiration date of the requested card
      required:
        - token
        - cardUniqueIdentifier
        - expirationDate
        - cardHolderName
        - tokenStatus
        - lastFourDigits
        - cardExpirationDate

    GetTokenDetails:
      type: object
      properties:
        token:
          type: string
          description: 'Token string generated for the given order (refNo)'
          example: 'd41d8cd98f00b204e9800998ecf8427e'
        cardUniqueIdentifier:
          description: 'Card unique identifier'
          type: string
          example: 'e9fc5107db302fa8373efbedf55a1614b5a3125ee59fe274e7dc802930d68f6d'
        expirationDate:
          type: string
          description: It is the date when the token expires. Should be in ISO_8601 YYYY-MM-DD format (https://en.wikipedia.org/wiki/ISO_8601).
          format: date
          example: '2023-06-10'
        cardHolderName:
          description: 'The card holder name'
          type: string
          example: 'Test'
        tokenStatus:
          description: 'The token status'
          type: string
          enum: [ 'ACTIVE', 'EXPIRED', 'CANCELED' ]
        lastFourDigits:
          type: string
          example: "1111"
          description: Last four digits of the requested card. If network tokenization is enabled on your account, then it will be the network token card's last four digits
        cardExpirationDate:
          type: string
          example: "2023-08-31"
          description: Expiration date of the requested card. If network tokenization is enabled on your account, then it will be the network token card's expiration date
        networkToken:
          type: object
          description: Available only if network tokenization is enabled on your account and only if a network token is available.
          properties:
            lastFourDigits:
              type: string
              example: "1111"
              description: Last four digits of the network token
            expirationDate:
              type: string
              example: "2023-08-31"
              description: The expiration date of the network token
            cardMedia:
              type: array
              description: Card media assets array (if network token doesn't have any card media assets, an empty array will be returned)
              items:
                type: object
                required:
                  - url
                  - type
                properties:
                  url:
                    type: string
                    description: Card media asset URL
                    example: https://media.paymentsos.com/live/8e49c2d7-9bff-4f8d-8144-cae60d932c7e_540.jpeg
                  type:
                    type: string
                    description: Card media asset type
                    example: "card"
                  width:
                    type: string
                    description: Media asset width
                    example: "540"
                  height:
                    type: string
                    description: Media asset height
                    example: "342"
          required:
            - lastFourDigits
            - expirationDate
            - cardMedia

      required:
        - token
        - cardUniqueIdentifier
        - expirationDate
        - cardHolderName
        - tokenStatus
        - lastFourDigits
        - cardExpirationDate

    StoredCredentialsResponse:
      type: object
      properties:
        useId:
          description: The transaction id in the card scheme system for this payment that can be used as an identifier of the customer consent to using stored payment credentials for processing subsequent payments. It should be stored when tokenization is handled externally and it should be sent in the subsequent authorization requests in the storedCredentials node. The availability of it depends on various factors related to processing acquirer and issuer so it should be handled as an optional value even when a consent was requested with consentType in the storedCredentials node in authorization request.
          type: string
          example: '123456'

    SessionsSuccessResponse:
      type: object
      properties:
        sessionId:
          description: The session id
          format: uuid
          example: "49a88d24-7615-41e8-adc0-fa7ae01bbebu"
        merchantCode:
          $ref: '#/components/schemas/MerchantCode'
        createdAt:
          type: string
          description: It is the datetime when the sessionId was generated. Should be in ISO_8601 Y-m-d\TH:i:sP format (https://en.wikipedia.org/wiki/ISO_8601).
          example: '2023-01-15T12:00:00+00:00'
        lifetimeMinutes:
          description: The session lifetime in minutes. This value will be received in the request or it will be the platform default
          format: number
          example: 10
          minimum: 1
          maximum: 60
        code:
          $ref: '#/components/schemas/200ResponseCode'
        message:
          $ref: '#/components/schemas/ResponseMessage'
        status:
          $ref: '#/components/schemas/SuccessResponseStatus'
      required:
        - sessionId
        - merchantCode
        - createdAt
        - lifetimeMinutes
        - code
        - message
        - status

    SessionsClientErrorResponse:
      allOf:
        - type: object
          properties:
            code:
              type: number
              enum: [ 400 ]
              description: "A error code (http code that is also returned in headers)"
            message:
              type: string
              example: "A text message with details about processing result or with some message error"
              description: "A text message with details about processing result or with some message error"
            status:
              type: string
              example: "INVALID_REQUEST"
              enum:
                - INVALID_REQUEST
          required:
            - code
            - message
            - status
    SessionsServerErrorResponse:
      allOf:
        - type: object
          properties:
            code:
              type: number
              enum: [ 500 ]
              description: "A error code (http code that is also returned in headers)"
            message:
              type: string
              example: "A text message with details about processing result or with some message error"
              description: "A text message with details about processing result or with some message error"
            status:
              type: string
              example: "INTERNAL_ERROR"
              enum:
                - INTERNAL_ERROR
          required:
            - code
            - message
            - status

    200ResponseCode:
      type: number
      enum: [ 200 ]
      description: "A Success code (http code that is also returned in headers)"

 ###END subnodes for request

  responses:
    200MerchantCreate:
      description: Successfully created merchant.
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/MerchantCreateResponse'

    TooManyRequestResponse:
      description: "Too many request. See API Limits."
      headers:
        'X-Rate-Limit-Limit':
          $ref: '#/components/headers/X-Rate-Limit-Limit'
        'X-Rate-Limit-Reset':
          $ref: '#/components/headers/X-Rate-Limit-Reset'
        'X-Rate-Limit-Remaining':
          schema:
            description: Contains value 0 (zero) because no request are available until X-Rate-Limit-Reset pass
            type: integer
            example: 0

      content:
        application/json:
          schema:
            type: object
            properties:
              code:
                description: "429"
                type: integer
                example: 429
              message:
                description: API calls limit reached. (0/0)
                type: string
                example: API calls limit reached. (0/0)
              status:
                description: A text representing the status of the response
                type: string
                enum:
                  - LIMIT_CALLS_EXCEEDED
                  - INVALID_REQUEST

    4xxResponse:
      description: "Request failed due to some invalid parameter."
      headers:
        'X-Rate-Limit-Limit':
          $ref: '#/components/headers/X-Rate-Limit-Limit'
        'X-Rate-Limit-Reset':
          $ref: '#/components/headers/X-Rate-Limit-Reset'
        'X-Rate-Limit-Remaining':
          $ref: '#/components/headers/X-Rate-Limit-Remaining'
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/BasicClientErrorsResponse'

    5xxResponse:
      description: "Request failed due to some internal errors. Please retry later."
      headers:
        'X-Rate-Limit-Limit':
          $ref: '#/components/headers/X-Rate-Limit-Limit'
        'X-Rate-Limit-Reset':
          $ref: '#/components/headers/X-Rate-Limit-Reset'
        'X-Rate-Limit-Remaining':
          $ref: '#/components/headers/X-Rate-Limit-Remaining'
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ServerErrorsResponse'
