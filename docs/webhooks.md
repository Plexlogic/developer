# Webhooks

Webhooks enables you to integrate Plexus gateway to external systems such as updating your Salesforce, Slack, calendar or even create a payment draft in Xero. Imagination is your limit.

When an event happens, we will send a HTTP POST request to your configured endpoint.

## Get started

Start configuring your webhook endpoint by contacting our Customer Success team.

Just tell us the event types you want to subscribe and your endpoint(s). We will give you a secret token for each subscription or you can specify your own.

## Events

You can subscribe to certain event types or all of them.

Each event is sent as a POST request to your HTTPS endpoint.

An example of the event payload:

```json
{
  // Event UUID
  "id": "8cfa669c-41cc-412c-858d-0374e2c007fc",
  // Event type
  "type": "DOCUMENT_UPDATED",
  // Event creation time, all timestamps are in ISO8601 format (UTC)
  "createdAt": "2021-11-11T22:39:59.250174+00:00",
  // "data" section is specific to each event type
  "data": {
    // ...
  }
}
```

### Document events types

1. `DOCUMENT_CREATED`
2. `DOCUMENT_UPDATED`
3. `DOCUMENT_DELETED`

Document event types share the same payload format.

```json
{
  "id": "8cfa669c-41cc-412c-858d-0374e2c007fc",
  "type": "DOCUMENT_UPDATED",
  "createdAt": "2021-11-11T22:39:59.250174+00:00",
  "data": {
    "document": {
      // Document type
      "type": "Service Agreement",
      "title": "Service Agreement for Company A",
      // Document status
      "status": "awaitingReview",
      "createdAt": "2021-09-02T04:37:56.812919+00:00",
      // Application that created this document
      "sourceApp": "Approve and eSign",
      // Start date specified in applications (e.g. Approve and eSign)
      "startDate": "2021-11-25",
      // Executed timestamp, null means it is not executed
      "executedAt": null,
      "expiryDate": "2021-11-27T13:00:00+00:00",
      // Specified at creation in applications (e.g. Approve and eSign)
      // You can use this externalId to track the document in your system (e.g. Salesforce)
      "externalId": "d24c0644-1d31-47fa-960e-b0cc8b4f136c",
      "ownerEmail": "owner@example.com",
      "authorEmail": "author@example.com",
      // TODO
      "referenceId": null,
      // Currency value of the contract
      // This can be specified in applications (e.g. Approve and eSign)
      // Currency will be an additional fact called "currency"
      "contractValue": 0,
      // This is the latest version that we have for this document
      // It can be a published or draft version
      "latestVersion": {
        "number": "7.1",
        "downloadUrl": "https://legalgateway-local.s3.amazonaws.com:443/media/documents/2499/Contract_2JS9d2q.docx"
      },
      // Additional document facts, these can be seen in the Document Facts tab in a document page
      "additionalFacts": {
        "customFact1": "abc",
        "customFact1": "123",
        "currency": "AUD"
      },
      "counterpartyName": "Company A",
      // This is the latest published version of the document
      "publishedVersion": {
        "number": "7.0",
        "downloadUrl": "https://legalgateway-local.s3.amazonaws.com:443/media/documents/2499/Contract_4JF72sf.docx"
      }
    }
  }
}
```

## Security

The endpoint receiving webhook events must be HTTPS.

Webhooks are protected by hash signatures. Each subscription has a secret token and each event includes a header `plexus-webhook-signature`, which is a HMAC hex digest of the payload calculated with the secret token using SHA512.

You should always verify the webhook event payload using this signature, this ensures that the message is sent by Plexus gateway and the payload is not tempered. You might also want to check the event `createdAt` to prevent replay attack.

Example Python code verifying the payload:

```python
import hmac
import hashlib

def verify_signature(payload_body, signature, secret_token):
    return hmac.compare_digest(
        signature,
        hmac.new(
            key=secret_token,
            msg=payload_body,
            digestmod=hashlib.sha512
        ).hexdigest()
    )
```

Note that using `==` is not advised, which is vulnerable to timing analysis. Please use a constant time secure comparison in your language similar to [`hamc.compare_digest`](https://docs.python.org/3/library/hmac.html#hmac.compare_digest).

## Technical details

We don’t 100% guarantee the events are sent in order, but we do have a `createdAt` timestamp on all the events.

When an event fails to be sent to your endpoint, we retry a few times. TODO ????

## Status mapping

TODO