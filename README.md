# ISO20022Gen

A Python library for generating ISO 20022 compliant financial messages, with a focus on FedWire Funds Service compatibility.

## About This Project

This open-source library focuses **exclusively** on generating the ISO 20022 XML content for financial messages. The library **does not generate the proprietary Fedwire envelope** which must be implemented separately according to Federal Reserve specifications.

For information on the proprietary Fedwire envelope format and specifications, please refer to the [Federal Reserve's ISO 20022 Implementation Center](https://www.frbservices.org/resources/financial-services/wires/iso-20022-implementation-center).

## Features

- Generate ISO 20022 compliant XML messages for financial transactions
- Support for pacs.008.001.08 message generation
- Validated against official ISO 20022 schemas
- Simple API for integrating with existing financial systems
- Command-line interface for direct usage

## Installation

```bash
pip install iso20022gen
```

## Quick Start

### Generating an ISO 20022 Message

```python
from iso20022gen import Iso20022CodeGen
import json

# Load your payment data
with open("payment_data.json", "r") as f:
    payment_data = json.load(f)

# Initialize the generator
generator = Iso20022CodeGen()

# Generate the ISO 20022 message
result = generator.process(payment_data)

if result["statusCode"] == 200:
    # Access the generated ISO 20022 XML
    iso_message = result["body"]
    print(iso_message)
```

### Command Line Usage

```bash
# Generate ISO 20022 message from payment data
iso20022gen generate payment_data.json
```

## Project Structure

- `code_generator.py`: The core ISO 20022 message generation functionality
- `config.py`: Configuration handling for the library

## Important Notice on Proprietary Envelope

The Fedwire envelope format is proprietary and must be implemented according to the Federal Reserve specifications. This library only generates the ISO 20022 message content (AppHdr and Document) that goes inside the envelope.

For official information about Fedwire ISO 20022 implementation, including envelope specifications, please consult the following resources:

- [Federal Reserve ISO 20022 Implementation Center](https://www.frbservices.org/resources/financial-services/wires/iso-20022-implementation-center)
- Federal Reserve's MyStandards platform (requires registration)
- The Fedwire Funds Service ISO 20022 Implementation Guide and Technical Guide

## Documentation

For detailed documentation, please visit our [documentation site](https://iso20022gen.readthedocs.io/).

## Input Format

The library expects payment data in a specific JSON format. Here's an example:

```json
{
  "fedWireMessage": {
    "inputMessageAccountabilityData": {
      "inputCycleDate": "20250109",
      "inputSource": "MBANQ001",
      "inputSequenceNumber": "000001"
    },
    "amount": {
      "amount": "000000001000"
    },
    "senderDepositoryInstitution": {
      "senderABANumber": "121182904",
      "senderShortName": "EXAMPLE BANK NAME"
    },
    "receiverDepositoryInstitution": {
      "receiverABANumber": "084106768",
      "receiverShortName": "RECEIVING BANK"
    },
    "beneficiary": {
      "personal": {
        "identificationCode": "D",
        "identifier": "9512227031535633",
        "name": "JOHN DOE",
        "address": {
          "addressLineOne": "123 MAIN STREET",
          "addressLineTwo": "ANYTOWN TX 12345"
        }
      }
    },
    "originator": {
      "personal": {
        "identificationCode": "D",
        "identifier": "550103129900943",
        "name": "JANE SMITH",
        "address": {
          "addressLineOne": "456 OAK AVENUE",
          "addressLineTwo": "SOMEWHERE CA 67890",
          "addressLineThree": ""
        }
      }
    }
  }
}
```

## Output

The library generates ISO 20022 compliant XML consisting of:
1. AppHdr - The ISO 20022 business application header
2. Document - The ISO 20022 pacs.008 document

**NOTE:** These XML components must be wrapped in the proprietary Fedwire envelope according to Federal Reserve specifications before being sent to the Fedwire Funds Service. The envelope generation is not part of this open-source project.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Install development dependencies (`pip install -e ".[dev]"`)
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

Please make sure your code adheres to our coding standards by running:

```bash
black iso20022gen tests
isort iso20022gen tests
flake8 iso20022gen tests
mypy iso20022gen tests
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- ISO 20022 Standard (www.iso20022.org)
- [Federal Reserve Financial Services](https://www.frbservices.org/) for Fedwire specifications 