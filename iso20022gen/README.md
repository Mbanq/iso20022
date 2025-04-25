# ISO 20022 Message Generator

This library provides functionality for generating ISO 20022 compliant XML messages based on a FedWire payload.

## Overview

ISO 20022 is a global standard for financial messaging that uses XML as its primary format. This library converts FedWire JSON payloads to ISO 20022 XML messages, specifically for pacs.008 (customer credit transfer) and AppHdr (application header).

## Installation

```bash
pip install -e .
```

## Usage

The library provides two approaches for generating ISO 20022 messages:

1. Dictionary-based approach (recommended)
2. Pydantic model-based approach

### Dictionary-based Approach

The dictionary-based approach uses simple Python classes with explicit to_dict() and from_payload() methods:

```python
import json
from iso20022gen.models.dict_models import AppHdr, Document
from iso20022gen.models.xml_converter import dict_to_xml, combine_xml_documents

# Load payload
with open("payload.json", "r") as f:
    payload = json.load(f)

# Create model objects
app_hdr = AppHdr.from_payload(payload)
document = Document.from_payload(payload)

# Convert to dict representation
app_hdr_dict = app_hdr.to_dict()
document_dict = document.to_dict()

# Convert to XML
app_hdr_xml = dict_to_xml(app_hdr_dict)
document_xml = dict_to_xml(document_dict)

# Combine XMLs
combined_xml = combine_xml_documents(app_hdr_xml, document_xml)

# Save to file
with open("output.xml", "w") as f:
    f.write(combined_xml)
```

### Pydantic Model-based Approach

The Pydantic-based approach uses Pydantic models with validators and schema definitions:

```python
import json
from iso20022gen.models.apphdr import AppHdr
from iso20022gen.models.pacs008 import Document
from iso20022gen.models.xml_converter import dict_to_xml, combine_xml_documents

# Load payload
with open("payload.json", "r") as f:
    payload = json.load(f)

# Create model objects
app_hdr = AppHdr.from_payload(payload)
document = Document.from_payload(payload)

# Convert to XML dict
app_hdr_dict = app_hdr.to_xml_dict()
document_dict = document.to_xml_dict()

# Convert to XML
app_hdr_xml = dict_to_xml(app_hdr_dict)
document_xml = dict_to_xml(document_dict)

# Combine XMLs
combined_xml = combine_xml_documents(app_hdr_xml, document_xml)

# Save to file
with open("output.xml", "w") as f:
    f.write(combined_xml)
```

## Command-line Usage

```bash
# Using the sample usage script
python -m iso20022gen.sample_usage iso20022gen/examples/sample_payment.json output.xml

# Using the test_models script
python -m iso20022gen.test_models iso20022gen/examples/sample_payment.json
```

## Model Structure

### AppHdr (Application Header)

The AppHdr contains metadata about the message, including:

- From (Fr): Sender financial institution
- To (To): Receiver financial institution
- Business Message ID (BizMsgIdr): Unique message identifier
- Message Definition ID (MsgDefIdr): Message type identifier (e.g., pacs.008.001.08)
- Business Service (BizSvc): Service identifier
- Market Practice (MktPrctc): Market practice information
- Creation Date (CreDt): Message creation timestamp

### Document (pacs.008)

The Document contains the actual payment information, including:

- Group Header (GrpHdr): Contains message identification and other group-level information
- Credit Transfer Transaction Information (CdtTrfTxInf): Contains the payment details
  - Payment ID (PmtId): End-to-end identifier and UETR
  - Interbank Settlement Amount (IntrBkSttlmAmt): Payment amount
  - Interbank Settlement Date (IntrBkSttlmDt): Settlement date
  - Debtor (Dbtr): Originator information
  - Debtor Account (DbtrAcct): Originator account information
  - Debtor Agent (DbtrAgt): Originator bank information
  - Creditor Agent (CdtrAgt): Beneficiary bank information
  - Creditor (Cdtr): Beneficiary information
  - Creditor Account (CdtrAcct): Beneficiary account information

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 