# ISO20022 Message Generator

A Python library for generating ISO20022 compliant financial messages, with a focus on FedWire Funds Service compatibility.

## Features

- Generate ISO20022 compliant XML messages
- Support for pacs.008 (FIToFICstmrCdtTrf) message type
- Automatic handling of namespaces and XML structure
- Clean XML output with no empty optional fields
- Support for both AppHdr and Document components

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/iso20022.git
cd iso20022

# Install in development mode
pip install -e .
```

## Usage

### Dictionary-based Approach

Here's an example of generating an ISO20022 message using the dictionary-based approach:

```python
import json
from dataclasses import asdict
from iso20022gen.models.apphdr import AppHdr
from iso20022gen.models.pacs008 import Document
from iso20022gen.models.xml_converter import dict_to_xml

# Load your payment data
with open("iso20022gen/examples/sample_payment.json", "r") as f:
    payload = json.load(f)

# Create AppHdr and Document objects
app_hdr = AppHdr.from_payload(payload)
document = Document.from_payload(payload)

# Convert to dictionaries
app_hdr_dict = asdict(app_hdr)
document_dict = asdict(document)

# Generate XML with proper namespaces
app_hdr_xml = dict_to_xml(
    app_hdr_dict,
    prefix="head",
    namespace="urn:iso:std:iso:20022:tech:xsd:head.001.001.03",
    root="AppHdr"
)
document_xml = dict_to_xml(
    document_dict,
    prefix="pacs",
    namespace="urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08",
    root="Document"
)

# Combine XMLs with XML declaration
xml_decl = '<?xml version="1.0" encoding="utf-8"?>'
combined_xml = f"{xml_decl}\n{app_hdr_xml}\n{document_xml}"

# Save to file
with open("output.xml", "w") as f:
    f.write(combined_xml)
```

### Sample Payload Format

Your input JSON should follow this structure:

```json
{
  "fedWireMessage": {
    "inputMessageAccountabilityData": {
      "inputCycleDate": "20250109",
      "inputSource": "MBANQ",
      "inputSequenceNumber": "001000001"
    },
    "amount": {
      "amount": "1000",
      "currency": "USD"
    },
    // ... other payment details
  }
}
```

## Features

- **Clean XML Output**: The library automatically removes empty optional fields from the XML output, ensuring clean and valid ISO20022 messages.
- **Namespace Handling**: Proper namespace prefixing and declarations are automatically managed.
- **Type Safety**: Uses Python dataclasses for type safety and validation.
- **Extensible**: Easy to add support for additional ISO20022 message types.

## Development

To run the tests:

```bash
python test_dict_approach.py
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.