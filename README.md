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

### From Source

1. Clone the repository:
```bash
git clone https://github.com/mbanq/iso20022gen.git
cd iso20022gen
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the package in development mode:
```bash
pip install -e .
```

## Quick Start

### Generating an ISO 20022 Message

The simplest way to test the message generation is using the standalone test script with a sample payload:

```bash
python standalone_test.py iso20022gen/examples/sample_payload.json
```

This will generate:
1. An ISO 20022 AppHdr (header) XML
2. A pacs.008.001.08 (credit transfer) Document XML
3. A combined output file named `output.xml`

### Sample Payload Format

The input JSON payload should follow this structure:
```json
{
    "fedWireMessage": {
        "inputMessageAccountabilityData": {
            "inputCycleDate": "20250109",
            "inputSource": "MBANQ",
            "inputSequenceNumber": "001000001"
        },
        "amount": {
            "amount": "1000"  // Amount in cents
        },
        "senderDepositoryInstitution": {
            "senderABANumber": "121182904",
            "senderShortName": "NORTH BAY CREDIT U"
        },
        "receiverDepositoryInstitution": {
            "receiverABANumber": "084106768",
            "receiverShortName": "EVOLVE BANK & TRUST"
        },
        "beneficiary": {
            "personal": {
                "name": "JOHN DOE",
                "identifier": "9512227031535633",
                "address": {
                    "addressLineOne": "123 MAIN STREET",
                    "addressLineTwo": "ANYTOWN, TX 12345"
                }
            }
        },
        "originator": {
            "personal": {
                "name": "JANE SMITH",
                "identifier": "550103129900943",
                "address": {
                    "addressLineOne": "456 OAK AVENUE",
                    "addressLineTwo": "SOMEWHERE, CA 67890"
                }
            }
        }
    }
}
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


## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- ISO 20022 Standard (www.iso20022.org)
- [Federal Reserve Financial Services](https://www.frbservices.org/) for Fedwire specifications 