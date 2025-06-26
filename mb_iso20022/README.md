# MB-ISO20022 Python Library

This package provides a set of tools for generating and working with ISO 20022 financial messages, with a special focus on the Fedwire Funds Service.

This library is the core component of the larger [ISO20022 Message Generator and Parser project](https://github.com/your-username/iso20022). For command-line tools and a web-based interface, please refer to the main project repository.

## Installation

You can install the package from PyPI:

```bash
pip install mb-iso20022
```

## Usage Examples

This section provides detailed examples for the core functionalities of the library.

**Index:**
- [Generating a `pacs.008.001.08` (Customer Credit Transfer) Message](#generating-a-pacs00800108-customer-credit-transfer-message)
- [Generating a `pacs.028.001.03` (Payment Status Request) Message](#generating-a-pacs02800103-payment-status-request-message)
- [Parsing a `pacs.008.001.08` XML to JSON](#parsing-a-pacs00800108-xml-to-json)
- [Parsing a `pacs.002.001.10` (Payment Status Report) XML to JSON](#parsing-a-pacs00200110-payment-status-report-xml-to-json)

---

### Generating a `pacs.008.001.08` (Customer Credit Transfer) Message

This example shows how to generate a Fedwire `pacs.008` message from a JSON payload.

```python
import json
from mb_iso20022.fedwire import generate_fedwire_message

# 1. Load your payment data from a JSON object
with open('sample_files/sample_payload.json', 'r') as f:
    payload = json.load(f)

# 2. Define the necessary message parameters
message_code = 'urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08'
fed_aba = '000000008' # The ABA number for the Fed
xsd_path = 'proprietary_fed_file.xsd' # The XSD file for fedwire format

# 3. Generate the complete XML message
xml_message = generate_fedwire_message(
    message_code=message_code,
    payload=payload,
    fed_aba=fed_aba,
    xsd_path=xsd_path
)

# 4. Save the message to a file
with open('generated_pacs.008.xml', 'w') as f:
    f.write(xml_message)

print("pacs.008.001.08 message generated successfully!")
```

### Generating a `pacs.028.001.03` (Payment Status Request) Message

This example shows how to generate a `pacs.028` payment status request.

```python
import json
from mb_iso20022.fedwire import generate_fedwire_message

# 1. Load the payload for the status request
with open('sample_files/sample_pacs028_payload.json', 'r') as f:
    payload = json.load(f)

# 2. Define message parameters
message_code = 'urn:iso:std:iso:20022:tech:xsd:pacs.028.001.03'
fed_aba = '000000008'
xsd_path = 'proprietary_fed_file.xsd'

# 3. Generate the XML message
xml_message = generate_fedwire_message(
    message_code=message_code,
    payload=payload,
    fed_aba=fed_aba,
    xsd_path=xsd_path
)

# 4. Save the message to a file
with open('generated_pacs.028.xml', 'w') as f:
    f.write(xml_message)

print("pacs.028.001.03 message generated successfully!")
```

### Parsing a `pacs.008.001.08` XML to JSON

This example shows how to parse a `pacs.008` XML file and convert it into a simplified JSON object.

```python
from mb_iso20022.fedwire import generate_fedwire_payload
import json

# 1. Define the path to your XML file and the message code
xml_file = 'sample_files/pacs.008.001.008_2025_1.xml'
message_code = 'pacs.008.001.08'

# 2. Parse the XML to get the JSON payload
payload_dict = generate_fedwire_payload(xml_file, message_code)

# 3. Save the payload to a JSON file
with open('parsed_pacs.008_payload.json', 'w') as f:
    json.dump(payload_dict, f, indent=4)

print("pacs.008.001.08 XML parsed to JSON successfully!")
```

### Parsing a `pacs.002.001.10` (Payment Status Report) XML to JSON

This example shows how to parse a `pacs.002` payment status report (ack/nack) into a JSON object.

```python
from mb_iso20022.fedwire import generate_fedwire_payload
import json

# 1. Define the path to your XML file and the message code
xml_file = 'sample_files/pacs.002_PaymentAck.xml'
message_code = 'pacs.002.001.10'

# 2. Parse the XML to get the JSON payload
payload_dict = generate_fedwire_payload(xml_file, message_code)

# 3. Save the payload to a JSON file
with open('parsed_pacs.002_payload.json', 'w') as f:
    json.dump(payload_dict, f, indent=4)

print("pacs.002.001.10 XML parsed to JSON successfully!")
```

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

Contributions are welcome! Please refer to the [main project repository](https://github.com/Mbanq/iso20022) for contribution guidelines, to open an issue, or to submit a pull request.
