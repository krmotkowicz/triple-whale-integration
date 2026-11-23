# triple-whale-integration

--------------------------------
Date: 23 Nov 2026
project: Assessment 
Triplewhale: Krystian Motkowicz
--------------------------------

# Triple Whale — Orders & Ads Data-In Integration

## 1. Project Overview

This project demonstrates a Python-based integration between a fictional e-commerce merchant Exampand Triple Whale using the Orders and Ads Data-In APIs.

The objective is to ingest synthetic commerce and advertising data, validate successful API responses, reconcile the ingested data against Triple Whale's reporting views, and explain how the integration could be made reliable in a production environment.

The implementation uses Python, REST APIs, JSON files, and GitHub Codespaces.

### Scope

- Submit individual order and advertising records using HTTP POST requests.
- Read multiple records from JSON files and submit them individually.
- Validate API responses and troubleshoot invalid requests.
- Verify ingested data in Triple Whale.
- Document field mappings, assumptions, reconciliation, security, and production-readiness considerations.

This is a data-in integration exercise. No separate application, dashboard, or data-out integration is required.

## 2. Fictional Merchant & Test Data

Sales platform: Custom

Shop id:`example123.com`

Reporting date: November 22 - 23, 2026

Currency: AUD

Timezone: Australia/Sydney (AEDT, UTC+11)

Dataset: Synthetic order and ads data only; no real customer information.

### Test Dataset

| Data source | Records | Expected amount |
|---|---:|---:|
| Orders | 6 | AUD $1,750 revenue | 
| Advertising | 4 campaigns | AUD $300.00 spend |

Orders were submitted through the Orders Data-In API. 
Advertising campaign records were submitted through the Ads Data-In API. 

Stable identifiers were used to distinguish records and support troubleshooting and reconciliation.

The reporting timezone is Australia/Sydney. Order timestamps were supplied in UTC, while advertising records use a reporting date. Date boundaries and timezone interpretation must be considered when comparing source data against platform reports.

## 3. Integration Architecture

The integration follows a simple data-in pattern:

Synthetic JSON data → Python scripts → Triple Whale REST Data-in API → Triple Whale Summary Dashboard

Each JSON record is submitted through an individual HTTP POST request. The scripts use the `requests` library to communicate with Triple Whale and print the HTTP status and API response.

Authentication uses the `TRIPLE_WHALE_API_KEY` environment variable rather than storing credentials in source code.

The integration demonstrates API ingestion and reporting validation. It does not establish customer-level advertising attribution.


### 3.1 Orders Data-In API

Endpoint: POST https://api.triplewhale.com/api/v2/data-in/orders

Source: Python dictionary for a single order, or files/orders_bulk.json for multiple orders.

Record grain: One commerce order per POST request.

Source field -> API field -> Purpose

Store identifier -> shop -> Identifies the merchant

Order identifier -> order_id -> Identifies the transaction

Order timestamp -> created_at -> Records when the order was created

Currency -> currency -> Identifies the monetary currency (e.g. AUD, USD) 

Customer identifier -> customer.id -> Associates an order with a customer

Customer email -> customer.email -> Provides customer's email identity

Order revenue -> order_revenue -> Records the order's revenue amount in currency 

The bulk-order script reads a JSON array and submits each order individually. It does not use Triple Whale's dedicated bulk-order endpoint.

### 3.2 Ads Data-In API

Endpoint: POST https://api.triplewhale.com/api/v2/data-in/ads

Source: Python dictionary for a single advertising record send_ads.py , or send_ads_file.py for multiple records.

Record grain: One campaign-level advertising record for a reporting date per POST request.

Source field -> API field -> Purpose

Store identifier -> shop -> Identifies the merchant

Advertising channel -> channel -> Identifies the advertising source

Reporting date -> event_date -> Associates metrics with a reporting date

Currency -> currency -> Identifies the spend currency

Campaign identifier -> campaign.id -> Identifies the advertising campaign

Campaign name -> campaign.name -> Provides a readable campaign name

Campaign status -> campaign.status -> Indicates ACTIVE or PAUSED

Advertising spend -> metrics.spend -> Records advertising investment


### 3.3 Relationships Between Orders and Ads

Orders and advertising records share the same merchant identifier.
However, the records do not contain a verified relationship between an individual advertising interaction and an order.
Additional click tracking, customer/session identity, and attribution configuration would be needed to connect advertising activity to individual conversions.

## 4. Setup and Execution Instructions

### 4.1 Prerequisites

The integration was developed and tested using:

- Python 3
- GitHub Codespaces
- Python `requests` library
- Triple Whale exercise store configured with Custom as the main sales platform
- Triple Whale API key with the required Data-In Orders and Ads Read permissions

No Shopify store, Node.js installation, or local development environment is required.

### 4.2 Install Dependencies

From the root directory of the GitHub repository, run:

```bash
python3 -m pip install -r requirements.txt
```

The `requirements.txt` file contains:

```text
requests
```

Python's built-in `json` and `os` modules require no additional installation.

### 4.3 Configure Authentication

The integration uses an environment variable named `TRIPLE_WHALE_API_KEY`.

In GitHub Codespaces, configure this as a Codespaces secret and make it available to the running environment.

The Python scripts retrieve the key using:

```python
import os

api_key = os.getenv("TRIPLE_WHALE_API_KEY")
```

Verify that the variable is available without displaying its value:

```bash
python3 -c "import os; print(bool(os.getenv('TRIPLE_WHALE_API_KEY')))"
```

Expected output:

```text
True
```

API credentials must never be committed to GitHub, hard-coded into scripts, or included in logs and screenshots.

### 4.4 Run the Orders Integration

**Send a single order:**

```bash
python3 send_orders.py
```

**Send multiple orders from a JSON file:**

```bash
python3 send_orders_file.py
```

The bulk script reads `files/orders_bulk.json` and sends one POST request per order.

### 4.5 Run the Ads Integration

**Send a single advertising record:**

```bash
python3 send_ads.py
```

**Send multiple advertising records from a JSON file:**

```bash
python3 send_ads_file.py
```

The advertising script reads `files/ads_single.json` using UTF-8 encoding:

```python
with open("files/ads_single.json", "r", encoding="utf-8") as file:
    ads = json.load(file)
```

Each advertising record is submitted through a separate POST request.

### 4.6 Validate JSON Files

Before submitting data, validate the JSON syntax:

```bash
python3 -m json.tool files/orders_bulk.json
python3 -m json.tool files/ads_bulk.json
```

Successful validation displays the formatted JSON without syntax errors.

This checks JSON syntax only. It does not validate the Triple Whale API schema.

### 4.7 Verify API Responses

The scripts display the HTTP status code and API response for each request.

An example of a successful advertising submission:

```text
HTTP status: 200
Response: {"success":true,"message":"Ad received"}
```

A successful HTTP response confirms API acceptance. Data correctness and reporting visibility must be verified separately inside Triple Whale.

## 5. API Validation, Error Handling and Troubleshooting

### 5.1 Validation Approach

The integration was tested incrementally to isolate issues before processing multiple records.
The following approach was used:
1. Validate the JSON file syntax.
2. Submit a single record using an HTTP POST request.
3. Inspect the HTTP status code and API response.
4. Correct any invalid or missing fields.
5. Retry the request and confirm successful API acceptance.
6. Submit multiple records from a JSON file.
7. Verify the resulting data inside Triple Whale Dashboards. 

This approach separates JSON syntax validation, API schema validation, and platform-level data reconciliation.

### 5.2 Controlled Failure — Invalid Advertising Campaign

During testing of the Ads Data-In API, the initial POST request returned HTTP 400.

**Endpoint:**

`POST https://api.triplewhale.com/api/v2/data-in/ads`

**First API response:**

```json
{
  "success": false,
  "message": [
    {
      "path": "campaign.name",
      "message": "Required"
    },
    {
      "path": "campaign.status",
      "message": "Campaign Status must be PAUSED or ACTIVE"
    }
  ]
}
```

**HTTP status:** `400 Bad Request`

The API identified two campaign-level validation failures:

- `campaign.name` was missing or not recognized as valid.
- `campaign.status` did not contain an accepted value.

The API required the campaign status to be either `ACTIVE` or `PAUSED`.

### 5.3 First Correction and Retry

The campaign status was corrected to `ACTIVE`.

The subsequent API response was:

```json
{
  "success": false,
  "message": [
    {
      "path": "campaign.name",
      "message": "Required"
    }
  ]
}
```

**HTTP status:** `400 Bad Request`

This demonstrated that the campaign status issue had been resolved, while the campaign name was still failing validation.

The next troubleshooting step was to inspect the outgoing JSON payload and verify the structure of the nested `campaign` object.

### 5.4 Successful Correction

The corrected campaign structure included the required fields:

```json
{
  "campaign": {
      "id": "001",
      "name": "November Fitness Campaign",
       "status": "ACTIVE"}
}
```

Following correction, the advertising request was accepted by Triple Whale.

**Successful API response:**

```json
{
  "success": true,
  "message": "Ad received"
}
```

**HTTP status:** `200 OK`

The same validated payload structure was then used for the JSON-file integration.

All three advertising records returned successful API responses.

The campaign structure above illustrates the required fields; the final evidence should include the complete sanitized payload actually submitted.

### 5.5 Bulk File Processing

The Python scripts read JSON arrays and submit records individually.
For example, the advertising integration processes each record using:

```python
for ad in ads:
    response = requests.post(
        url,
        headers=headers,
        json=ad,
        timeout=20
    )

    print("HTTP status:", response.status_code)
    print("Response:", response.text)
```

Each POST request produces an independent API response.

This allows individual failures to be identified without treating the entire file as a single API transaction.

The current implementation prints responses but does not yet implement automatic retries, persistent failure logging, or checkpoint-based recovery.


### 5.6 Security Considerations

API credentials are stored in GitHub Codespaces secrets and accessed through the `TRIPLE_WHALE_API_KEY` environment variable.

Credentials are not included in source code, JSON files, request evidence, or screenshots.

## 6. Platform Validation and Reconciliation

### 6.1 Validation Objective

The objective of reconciliation is to confirm that the synthetic commerce and advertising data submitted through the Triple Whale Data-In APIs appears correctly in the platform.

Validation was performed at three levels:

1. **Source validation:** Confirm the records and expected values in the original payloads.
2. **API validation:** Confirm successful HTTP responses from Triple Whale.
3. **Platform validation:** Compare ingested data against the available Triple Whale reporting views.

A successful HTTP 200 response confirms API acceptance but does not independently prove that reporting values are correct.

### 6.2 Orders Reconciliation

Six synthetic orders were submitted using the Orders Data-In API.
One order was submitted individually, followed by four orders read from `files/orders_bulk.json`.

| Metric | Expected | Observed |
|---|---:|---:|
| Order count | 6 | 6 |
| Total order revenue | AUD $1,750 | AUD $1,750 |

**Result:** The order count, revenue total count matched the values observed in Triple Whale during testing.
The advertising data was subsequently confirmed as visible in Triple Whale.

### 6.3 Adds Reconciliation

Four synthetic advertising records are included in the reported test dataset, representing a total advertising investment of AUD $300.
The advertising data was submitted using the Triple Whale Ads Data-In API

Individual advertising records were tested separately, and multiple records were processed from JSON files using Python.

| Metric | Expected | Observed |
|---|---:|---:|
| Adds count | 4 | 4|
| Total adds cost | AUD $300 | AUD $300 |

Result: The README records a match between expected advertising spend and the values observed in Triple Whale.
API acceptance was validated through HTTP 200 responses. Platform reconciliation was performed separately using Triple Whale reporting views.

Important: Advertising ingestion provides visibility into marketing expenditure but does not independently establish customer-level attribution or attributed ROAS.

## 7. Solutions Architecture and Production Reliability

### 7.1 Architecture Overview

The exercise implements a lightweight Python integration between a fictional commerce platform and Triple Whale.

**Current implementation:**

`Synthetic JSON files → Python scripts → Triple Whale Data-In APIs → Platform reporting views`

The solution separates two data domains:

- **Commerce data:** Orders, customers, transaction timestamps, and revenue.
- **Advertising data:** Campaign identifiers, reporting dates, campaign status, and advertising spend.

Each record is submitted through an individual authenticated HTTP POST request.

This design is sufficient to demonstrate the required ingestion and validation workflow. It is not intended to be a production-grade data pipeline.

### 7.2 Why Order Data Matters

Orders provide the transactional foundation for understanding commerce performance.

Reliable order data enables a platform to understand:

- Sales volume and revenue over time.
- Customer purchasing behavior and repeat purchases.
- Transaction-level revenue and customer relationships.
- Changes in commerce performance across reporting periods.

For a real merchant, revenue definitions must be agreed upon before implementation.

For example, gross sales, discounts, refunds, taxes, shipping, and net revenue may produce different financial totals.


### 7.3 Why Advertising Data Matters

Advertising data provides visibility into marketing investment and campaign performance.

Campaign identifiers, reporting dates, spend, and delivery metrics help explain how advertising budgets are allocated and how performance changes over time.

Accurate advertising data supports:

- Campaign-level spend reporting.
- Comparison of advertising investment across reporting periods.
- Monitoring marketing efficiency.
- Identification of unexpected changes in spend or campaign delivery.

The reporting grain must be explicitly defined.

For this exercise, advertising data is represented at **campaign-by-reporting-date grain**.

If a source provides multiple rows for the same campaign and date, the integration must determine whether those rows represent distinct dimensions, updates, or duplicates before submission.

For production, additional supported delivery metrics such as impressions and clicks would be useful for calculating CTR and CPC. These metrics were not established as successfully ingested in the current exercise.

Incorrect campaign IDs, dates, spend amounts, or record grain could cause duplicated spend, missing campaigns, or misleading performance comparisons.

### 7.4 Ingestion Is Not Attribution

Successfully ingesting order and advertising data does not prove that a particular advertisement generated a particular order.
Orders represent transactions. Advertising records represent media investment and delivery.
To establish attribution, a merchant would need additional evidence such as:
- Website or server-side conversion tracking.
- Advertising click identifiers and UTM parameters.
- Consistent session, customer, and order identifiers.
- Appropriate tracking and attribution configuration.
- Defined conversion windows and attribution models.
- Reconciliation between tracked conversions and actual commerce orders.

**Attributed ROAS = attributed revenue / advertising spend.**

Attributed ROAS is not the same as profit.

### 7.5 Production Reliability Design

A production implementation would introduce additional controls beyond the current Python scripts.

| Area | Recommended design |
|---|---|
| Schema validation | Validate required fields, data types, currencies, timestamps, and supported enumerations before API submission |
| Stable identifiers | Preserve source order and campaign IDs consistently |
| Duplicate prevention | Follow documented endpoint update and deduplication behavior |
| Retries | Retry eligible transient failures with exponential backoff and jitter |
| Rate limiting | Respect API rate limits and `Retry-After` guidance where provided |
| Partial failures | Track the outcome of each submitted record |
| Backfills | Support controlled historical reprocessing by date range |
| Updates | Process order lifecycle changes and revised advertising metrics |
| Monitoring | Track request failures, processing delays, record counts, and financial totals |
| Reconciliation | Compare source and platform values using consistent reporting definitions |

Retries must be designed carefully.
For example, an HTTP 400 validation error should not be retried unchanged. A timeout may require checking whether the original request was processed before attempting another submission.

### 7.6 Optional API Extensions

The exercise requires Orders and Ads Data-In APIs. Additional endpoints could provide useful context for a real merchant.

| Optional endpoint | Business value |
|---|---|
| Products | Enrich order analysis with catalog and product identifiers |
| Customers | Support consistent customer identity and lifecycle analysis |
| Subscriptions | Provide recurring revenue and subscription lifecycle context |
| Email/SMS | Include messaging campaign and flow performance |
| Post-Purchase Surveys (PPS) | Add customer-reported attribution signals |

These endpoints were not implemented in the current exercise.
Their suitability would depend on the merchant's business model, available source data, and reporting objectives.

## 9. Known Limitations, Submission Evidence, and Final Checklist

### 9.1 Known Limitations

This project is a technical demonstration using a fictional merchant and synthetic data. It is not a production integration.

| Area | Limitation | Production recommendation |
|---|---|---|
| Data ingestion | JSON records submitted through individual POST requests | Introduce scheduled or event-driven ingestion |
| Error handling | HTTP status codes and responses printed to the terminal | Persist sanitized request and response logs |
| Retries | No automatic retry mechanism | Implement controlled retries for transient errors |
| Duplicate handling | Repeat submissions not systematically tested | Verify endpoint-specific update and deduplication behavior |
| Schema validation | JSON syntax validated manually | Introduce automated API schema validation |
| Reconciliation | Manual verification in Triple Whale | Automate source-to-platform reconciliation |
| Monitoring | No automated alerts | Monitor failures, delays, and discrepancies |
| Attribution | No customer journey or ad-click tracking implemented | Integrate tracking and identity signals where supported |
| Data coverage | Limited synthetic records and reporting dates | Support incremental ingestion, updates, and historical backfills |
| Security | API key managed through Codespaces secrets | Add credential rotation, least-privilege access, and audit controls |

These limitations are intentional for a focused technical exercise.

The implementation demonstrates successful ingestion, troubleshooting, and platform validation while identifying the additional controls required for a production environment.

## 10 Submission Artifacts
The GitHub repository contains or will contain the following deliverables.

| Artifact | Purpose |
|---|---|
| `README.md` | Project overview, setup, field mappings, validation, architecture, and limitations |
| `requirements.txt` | Python dependencies |
| `test_api.py` | API test |
| `send_single_order.sh` | Shell Script to send test single order |
| `send_orders_file.py` | Multiple order submissions from a JSON file "orders_bulk.json" |
| `send_orders.py` | Single order record submission "orders_single.json" |
| `send_ads_file.py` | Python scritp with multiple advertising submissions from a JSON file "ads_bulk.json"|
| `send_ads.py` | Python scritp with single advertising submissions from a JSON file "ads_single"|
| `files/ads_bulk.json` | Synthetic ads bulk json dataset |
| `files/ads.json` | Synthetic single ad JSON file |
| `files/orders_bulk.json` | Synthetic multiple ads JSON file |
| `files/orders_single.json` | Synthetic single ad JSON file |

The repository should not contain API credentials, real customer data, or production account information.

**Successful Ads Data-In**

- Single advertising record POST request.
- Three advertising records submitted from a JSON file.
- HTTP 200 responses confirming acceptance.
- Sanitized payloads and request timestamps, where recorded
- Dashboard numbers match the ads and orders files

  ## END ##
