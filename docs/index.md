# Webhooks

Plexus Gateway uses webhooks to allow your application to receive information about document events as they occur. You can then choose how your application responds in a variety of ways, or use webhooks to integrate Plexus Gateway with third party systems. Update a lead in Salesforce, send a Slack notification, create a Google Calendar event or create a draft payment in Xero - our extensible framework is here to support any way of working. This documentation will detail configuring webhooks, event types and technological specifications to get you started. 

## Get started

You can start receiving document event notifications in your app by:

1. Identify the events you want to monitor and create your webhook endpoint as an HTTPS endpoint (URL)
2. Get in touch with your Customer Success Manager
3. Plexus will then provide you with a secret token for each subscription, or you can specify your own

## Events

You can subscribe to any number of events through webhooks. Each event is sent as a POST request to your HTTPS endpoint. 

Every event payload includes the following event attributes:

| Attribute | Description |
| --- | --- |
| `id` | Event UUID |
| `type` | Event type |
| <span id="event-created-at">`createdAt`</span> | Event creation time. All timestamps are in ISO8601 format (UTC): `YYYY-MM-DDTHH:MM:SS.ffffff+HH:MM` |
| `data` | The `data` section varies according to the type of event |

This example outlines their format and structure:

```json title="Event payload example"
{
  "id": "8cfa669c-41cc-412c-858d-0374e2c007fc",
  "type": "documentUpdated",
  "createdAt": "2021-11-11T22:39:59.250174+00:00",
  "data": {
    // ...
  }
}
```

### Document event types

Documents have three event types, each of which will create different content in the data section of the payload:

1. `documentCreated`
2. `documentUpdated`
3. `documentDeleted`

### Document attributes

Each event contains additional document attributes:

| Attribute | Description |
| --- | --- |
| `type` | Document type |
| `title` | Document title |
| `status` | [Document status](#document-status) |
| `createdAt` | Document creation timestamp |
| `sourceApp` | The app inside Plexus Gateway that created this document |
| `startDate` | The start date that was specified when the document was created, or in the facts view tab on the document details page |
| `executedAt` | The date the document was executed. If the document has not been executed, this field will be null |
| `expiryDate` | The expiry date that was specified when the document was created, or in the facts view tab on the document details page |
| `externalId` | UUID created by Plexus Gateway |
| `ownerEmail` | The document owner’s email address |
| `authorEmail` | The document author’s email address |
| `referenceId` | An identifier assigned to the document when it is created with an app inside Plexus Gateway. You can use this referenceId to track the document in your app or another third party system, such as SalesForce |
| `contractValue` | The monetary value of the document that was specified when the document was created, or in the facts view tab on the document details page |
| `latestVersion` | The latest version of the document, either published or as a draft |
| `additionalFacts` | Additional facts containing information added to the document in the facts view tab on the document details page. This is a JSON object of fact name-value pairs |
| `counterpartyName` | Name of the document’s counterparty. If the document has no counterparty, this field will be null |
| `publishedVersion` | The latest published version of the document |

The `latestVersion` and `publishedVersion` attributes contain the following sub-attributes:

| Sub-attribute | Description |
| --- | --- |
| `number` | Version number |
| `downloadUrl` | Download URL, valid for 15 minutes from [event creation](#event-created-at) |

### Document status

Webhook document event statuses provide you information about the current state of the document as it progresses through the document workflow:

| Status | Description |
| --- | --- |
| `created` | Document has been created |
| `awaitingReview` | Document is awaiting a review |
| `reviewApproved` | Review approved |
| `reviewRejected` | Review rejected |
| `awaitingApproval` | Document at the start of the approval phase |
| `approved` | Document approval phase completed by all approvers |
| `approvalRejected` | Document approval phase rejected by one or more approvers |
| `awaitingSignature` | Document at the start of the signature phase |
| `signedByClient` | Legacy document status retained for backwards compatibility |
| `signatureRejected` | Document sigtaure phase rejected by one or more signers |
| `signatureRequestExpired` | Document signature phase expired |
| `executed` | Document fully executed |
| `paused` | Document workflow has been paused |
| `cancelled` | Document workflow has been cancelled |
| `other` | Legacy document statuses may result in an `other` status |

### Bringing it all together

These examples show how all document attributes are formatted in one payload:

=== "`documentCreated`"

    ```json
    {
      "id": "8cfa669c-41cc-412c-858d-0374e2c007fc",
      "type": "documentCreated",
      "createdAt": "2021-11-11T22:39:59.250174+00:00",
      "data": {
        "document": {
          "type": "Service Agreement",
          "title": "Service Agreement for Company A",
          "status": "created",
          "createdAt": "2021-09-02T04:37:56.812919+00:00",
          "sourceApp": "Approve and eSign",
          "startDate": "2021-11-25",
          "executedAt": null,
          "expiryDate": "2021-11-27T13:00:00+00:00",
          "externalId": "d24c0644-1d31-47fa-960e-b0cc8b4f136c",
          "ownerEmail": "owner@example.com",
          "authorEmail": "author@example.com",
          "referenceId": null,
          "contractValue": 0.0,
          "latestVersion": {
            "number": "7.1",
            "downloadUrl": "https://legalgateway-local.s3.amazonaws.com:443/media/documents/2499/Contract_2JS9d2q.docx?..."
          },
          "additionalFacts": {
            "customFact1": "abc",
            "customFact1": "123",
            "currency": "AUD"
          },
          "counterpartyName": "Company A",
          "publishedVersion": {
            "number": "7.0",
            "downloadUrl": "https://legalgateway-local.s3.amazonaws.com:443/media/documents/2499/Contract_4JF72sf.docx?..."
          }
        }
      }
    }
    ```

=== "`documentUpdated`"

    ```json
    {
      "id": "8cfa669c-41cc-412c-858d-0374e2c007fc",
      "type": "documentUpdated",
      "createdAt": "2021-11-11T22:39:59.250174+00:00",
      "data": {
        "document": {
          "type": "Service Agreement",
          "title": "Service Agreement for Company A",
          "status": "awaitingReview",
          "createdAt": "2021-09-02T04:37:56.812919+00:00",
          "sourceApp": "Approve and eSign",
          "startDate": "2021-11-25",
          "executedAt": null,
          "expiryDate": "2021-11-27T13:00:00+00:00",
          "externalId": "d24c0644-1d31-47fa-960e-b0cc8b4f136c",
          "ownerEmail": "owner@example.com",
          "authorEmail": "author@example.com",
          "referenceId": null,
          "contractValue": 0.0,
          "latestVersion": {
            "number": "7.1",
            "downloadUrl": "https://legalgateway-local.s3.amazonaws.com:443/media/documents/2499/Contract_2JS9d2q.docx?..."
          },
          "additionalFacts": {
            "customFact1": "abc",
            "customFact1": "123",
            "currency": "AUD"
          },
          "counterpartyName": "Company A",
          "publishedVersion": {
            "number": "7.0",
            "downloadUrl": "https://legalgateway-local.s3.amazonaws.com:443/media/documents/2499/Contract_4JF72sf.docx?..."
          }
        }
      }
    }
    ```

=== "`documentDeleted`"

    ```json
    {
      "id": "8cfa669c-41cc-412c-858d-0374e2c007fc",
      "type": "documentDeleted",
      "createdAt": "2021-11-11T22:39:59.250174+00:00",
      "data": {
        "document": {
          "type": "Service Agreement",
          "title": "Service Agreement for Company A",
          "status": "other",
          "createdAt": "2021-09-02T04:37:56.812919+00:00",
          "sourceApp": "Approve and eSign",
          "startDate": "2021-11-25",
          "executedAt": null,
          "expiryDate": "2021-11-27T13:00:00+00:00",
          "externalId": "d24c0644-1d31-47fa-960e-b0cc8b4f136c",
          "ownerEmail": "owner@example.com",
          "authorEmail": "author@example.com",
          "referenceId": null,
          "contractValue": 0.0,
          "latestVersion": {
            "number": "7.1",
            "downloadUrl": "https://legalgateway-local.s3.amazonaws.com:443/media/documents/2499/Contract_2JS9d2q.docx?..."
          },
          "additionalFacts": {
            "customFact1": "abc",
            "customFact1": "123",
            "currency": "AUD"
          },
          "counterpartyName": "Company A",
          "publishedVersion": {
            "number": "7.0",
            "downloadUrl": "https://legalgateway-local.s3.amazonaws.com:443/media/documents/2499/Contract_4JF72sf.docx?..."
          }
        }
      }
    }
    ```

### Message order and built-in retries

We provide a loose capability that attempts to preserve the order of messages. However, receiving messages in the exact order they are sent is not guaranteed. Use the [`createdAt`](#event-created-at) timestamp on all the events to determine the order.

For each POST request for an event, we have a 5-second timeout.
If an event cannot be sent to your endpoint, we will retry 3 times before giving up.

## Configuration and security

To set up webhooks, the customer support team needs the following information:

1. HTTPS URL(s) which events will be sent to
1. Which events will be sent (`documentCreated`, `documentUpdated`, and/or `documentDeleted`)
1. List of additional headers which will be passed to the URL (optional)

For security, each webhook also has a secret token which can be used to verify events have been sent by Plexus. This is used to generate an HMAC-SHA256 signature for the payload, provided by the `plexus-webhook-signature` header. Example code to verify the signature is shown below:

```python
import hmac
import hashlib

def verify_signature(payload, headers, secret_token):
    actual_signature = headers["plexus-webhook-signature"]
    expected_signature = hmac.new(
        key=secret_token,
        msg=payload,
        digestmod=hashlib.sha512
    ).hexdigest()
    
    return hmac.compare_digest(actual_signature, expected_signature)
```

For security reasons, you should avoid verifying the signature using equality operators (see [here](https://docs.python.org/3/library/hmac.html#hmac.compare_digest)). You may also want to use the event `createdAt` field to prevent replay attacks.
