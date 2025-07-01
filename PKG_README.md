# MISO20022 Python Library

This package provides a set of tools for generating and working with ISO 20022 financial messages, with a focus on the US Payment Rails.


## Installation

You can install the package from PyPI:

```bash
pip install miso20022
```

## Usage Examples

This section provides detailed examples for the core functionalities of the library.

**Index:**
- [Generating a `pacs.008.001.08` (Customer Credit Transfer) Message](#generating-a-pacs00800108-customer-credit-transfer-message)
- [Generating a `pacs.028.001.03` (Payment Status Request) Message](#generating-a-pacs02800103-payment-status-request-message)
- [Parsing a `pacs.008.001.08` XML to JSON](#parsing-a-pacs00800108-xml-to-json)
- [Parsing a `pacs.002.001.10` (Payment Status Report) XML to JSON](#parsing-a-pacs00200110-payment-status-report-xml-to-json)

---

### Input JSON Structure

The `generate_fedwire_message` function expects a specific JSON structure for the `payload` argument. Below are the expected formats for the supported message types.

#### `pacs.008.001.08` (Customer Credit Transfer)

The payload for a `pacs.008` message should follow this structure:

```json
{
  "fedWireMessage": {
    "inputMessageAccountabilityData": {
      "inputCycleDate": "20250109",
      "inputSource": "MBANQ",
      "inputSequenceNumber": "001000001"
    },
    "amount": {
      "amount": "1000"
    },
    "senderDepositoryInstitution": {
      "senderABANumber": "<routing_number>",
      "senderShortName": "Pypi Bank"
    },
    "receiverDepositoryInstitution": {
      "receiverABANumber": "<routing_number>",
      "receiverShortName": "HelloBank"
    },
    "originator": {
      "personal": {
        "name": "JANE SMITH",
        "address": {
          "addressLineOne": "456 eat street",
          "addressLineTwo": "SOMEWHERE, CA 67890",
          "addressLineThree": ""
        },
        "identifier": "<account_number>"
      }
    },
    "beneficiary": {
      "personal": {
        "name": "JOHN DOE",
        "address": {
          "addressLineOne": "123 Main street",
          "addressLineTwo": "ANYTOWN, TX 12345",
          "addressLineThree": ""
        },
        "identifier": "<account_number>"
      }
    }
  }
}
```

#### `pacs.028.001.03` (Payment Status Request)

The payload for a `pacs.028` message should follow this structure:

```json
{
  "fedWireMessage": {
    "inputMessageAccountabilityData": {
      "inputCycleDate": "20250109",
      "inputSource": "MBANQ",
      "inputSequenceNumber": "001000002"
    },
    "senderDepositoryInstitution": {
      "senderABANumber": "<routing_number>",
      "senderShortName": "<short_name>"
    },
    "receiverDepositoryInstitution": {
      "receiverABANumber": "<routing_number>",
      "receiverShortName": "<short_name>"
    }
  },
  "message_id": "PACS028REQ20250109001",
  "original_msg_id": "20250109MBANQ001000001",
  "original_msg_nm_id": "pacs.008.001.08",
  "original_creation_datetime": "2025-01-09T12:34:56Z",
  "original_end_to_end_id": "MEtoEIDCJShqZKb"
}
```

### Generating a `pacs.008.001.08` (Customer Credit Transfer) Message

This example shows how to generate a Fedwire `pacs.008` message from a JSON payload.

```python
import json
from miso20022.fedwire import generate_fedwire_message

# 1. Load your payment data from a JSON object
with open('sample_files/sample_payload.json', 'r') as f:
    payload = json.load(f)

# 2. Define the necessary message parameters
message_code = 'urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08'
environment = "TEST"  # Or "PROD"
fed_aba = '000000008' # The ABA number for the Fed
xsd_path = 'proprietary_fed_file.xsd' # The XSD file for fedwire format

# 3. Generate the complete XML message
_, _, complete_message = generate_fedwire_message(
    message_code=message_code,
    environment=environment,
    fed_aba=fed_aba,
    payload=payload,
    xsd_path=xsd_path
)

# 4. The `complete_message` variable now holds the XML string
if complete_message:
    print(complete_message)
```

### Generating a `pacs.028.001.03` (Payment Status Request) Message

This example shows how to generate a `pacs.028` payment status request.

```python
import json
from miso20022.fedwire import generate_fedwire_message

# 1. Load the payload for the status request
with open('sample_files/sample_pacs028_payload.json', 'r') as f:
    payload = json.load(f)

# 2. Define message parameters
message_code = 'urn:iso:std:iso:20022:tech:xsd:pacs.028.001.03'
environment = "TEST"  # Or "PROD"
fed_aba = '000000008'
xsd_path = 'proprietary_fed_file.xsd'

# 3. Generate the XML message
_, _, complete_message = generate_fedwire_message(
    message_code=message_code,
    environment=environment,
    fed_aba=fed_aba,
    payload=payload,
    xsd_path=xsd_path
)

# 4. The `complete_message` variable now holds the XML string
if complete_message:
    print(complete_message)
```

### Parsing a `pacs.008.001.08` XML to JSON

This example shows how to parse a `pacs.008` XML file and convert it into a simplified JSON object.

```python
from miso20022.fedwire import generate_fedwire_payload
import json

# 1. Define the path to your XML file and the message code
xml_file = 'incoming_pacs.008.xml'
message_code = 'urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08'

# 2. Parse the XML file
fedwire_json = generate_fedwire_payload(xml_file, message_code)

# 3. The `fedwire_json` variable now holds the parsed dictionary
if fedwire_json:
    print(json.dumps(fedwire_json, indent=4))
```

### Parsing a `pacs.002.001.10` (Payment Status Report) XML to JSON

This example shows how to parse a `pacs.002` payment status report (ack/nack) into a JSON object.

```python
from miso20022.fedwire import generate_fedwire_payload
import json

# 1. Define the path to your XML file and the message code
xml_file = 'sample_files/pacs.002_PaymentAck.xml'
message_code = 'urn:iso:std:iso:20022:tech:xsd:pacs.002.001.10'

# 2. Parse the XML to get the JSON payload
fedwire_json = generate_fedwire_payload(xml_file, message_code)

# 3. The `fedwire_json` variable now holds the parsed dictionary
if fedwire_json:
    print(json.dumps(fedwire_json, indent=4))
```

## Command-Line Interface (CLI)

The package includes a command-line tool, `miso20022`, for generating and parsing messages directly from your terminal.

### Generating a Message

**Usage:**

```bash
miso20022 generate --message_code [MESSAGE_CODE] --environment [ENV] --fed-aba [ABA_NUMBER] --input-file [PAYLOAD_FILE] --output-file [OUTPUT_XML]
```

**Arguments:**

-   `--message_code`: The ISO 20022 message code (e.g., `urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08`).
-   `--environment`: The environment for the message (`TEST` or `PROD`).
-   `--fed-aba`: The Fedwire ABA number.
-   `--input-file`: Path to the input JSON payload file.
-   `--output-file`: (Optional) Path to save the generated XML message.
-   `--xsd-file`: (Optional) Path to the XSD file for validation.

**Example:**

```bash
miso20022 generate \
    --message_code urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08 \
    --environment TEST \
    --fed-aba 000000008 \
    --input-file sample_files/sample_payment.json \
    --output-file pacs.008_output.xml
```

### Parsing a Message

**Usage:**

```bash
miso20022 parse --input-file [INPUT_XML] --message-code [MESSAGE_CODE] --output-file [OUTPUT_JSON]
```

**Arguments:**

-   `--input-file`: Path to the input ISO 20022 XML file.
-   `--message-code`: The ISO 20022 message code of the input file.
-   `--output-file`: (Optional) Path to save the output JSON payload.

**Example:**

```bash
miso20022 parse \
    --input-file sample_files/pacs.008.001.008_2025_1.xml \
    --message-code urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08 \
    --output-file parsed_payload.json
```

---

## Supported Message Types

The library provides different levels of support for various message types.

### Message Generation (`generate_fedwire_message`)

The following message types are fully supported with dedicated data models for generating complete XML messages:

-   **`pacs.008.001.08`**: FI to FI Customer Credit Transfer
-   **`pacs.028.001.03`**: FI to FI Payment Status Request

While other message types might be generated using the generic handlers, these are the ones with first-class support.

### XML to JSON Parsing (`generate_fedwire_payload`)

The library can parse the following XML message types into a simplified Fedwire JSON format:

-   **`pacs.008.001.08`**: FI to FI Customer Credit Transfer
-   **`pacs.002.001.10`**: FI to FI Payment Status Report

Support for parsing other message types can be added by creating new mapping functions.

### Future Support

We are actively working to expand the range of supported message types. Future releases will include built-in support for additional `pacs`, `camt`, and other ISO 20022 messages, with planned support for FedNow services. Stay tuned for updates!

## Contributing

Contributions are welcome! Please refer to the [Project repository](https://github.com/Mbanq/iso20022) for contribution guidelines, to open an issue, or to submit a pull request.

<p align="center"><strong style="font-size: 2em">Built with ❤️ in the Beautiful State of Washington!</strong></p>


