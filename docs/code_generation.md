# ISO 20022 Code Generation Process

This document explains the process of generating ISO 20022 compliant messages in the iso20022gen library.

## Overview

ISO 20022 is a global standard for financial messaging that uses XML as its primary format. The iso20022gen library provides functionality to generate these XML messages based on input JSON data representing financial transactions.

## Message Generation Process

The process of generating an ISO 20022 message involves several steps:

1. **Input Data Validation**: The library first validates the input JSON data to ensure all required fields are present and well-formatted.

2. **XML Structure Creation**: The library creates the XML structure according to the ISO 20022 specifications.

3. **Data Mapping**: Data from the input JSON is mapped to the corresponding XML elements.

4. **XML Validation**: The generated XML is validated against the official ISO 20022 XSD schemas to ensure compliance.

5. **Optional Fedwire Wrapping**: If requested, the XML can be wrapped in a Fedwire envelope according to Federal Reserve specifications.

## XML Structure

An ISO 20022 message consists of two main parts:

1. **AppHdr (Application Header)**: Contains metadata about the message, including sender, receiver, and message type.

2. **Document**: Contains the actual financial data, such as the payment details.

### AppHdr Structure

The AppHdr element follows this structure:

```xml
<AppHdr xmlns="urn:iso:std:iso:20022:tech:xsd:head.001.001.03">
    <Fr>
        <!-- Sender details -->
    </Fr>
    <To>
        <!-- Receiver details -->
    </To>
    <BizMsgIdr>
        <!-- Message ID -->
    </BizMsgIdr>
    <MsgDefIdr>
        <!-- Message definition ID -->
    </MsgDefIdr>
    <BizSvc>
        <!-- Business service -->
    </BizSvc>
    <CreDt>
        <!-- Creation date/time -->
    </CreDt>
</AppHdr>
```

### Document Structure

The Document element structure depends on the message type. For a customer credit transfer (pacs.008), it follows this structure:

```xml
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08">
    <FIToFICstmrCdtTrf>
        <GrpHdr>
            <!-- Group header information -->
        </GrpHdr>
        <CdtTrfTxInf>
            <!-- Credit transfer information -->
            <PmtId>
                <!-- Payment identification -->
            </PmtId>
            <IntrBkSttlmAmt>
                <!-- Settlement amount -->
            </IntrBkSttlmAmt>
            <Dbtr>
                <!-- Debtor (originator) information -->
            </Dbtr>
            <DbtrAcct>
                <!-- Debtor account information -->
            </DbtrAcct>
            <DbtrAgt>
                <!-- Debtor agent (bank) information -->
            </DbtrAgt>
            <CdtrAgt>
                <!-- Creditor agent (bank) information -->
            </CdtrAgt>
            <Cdtr>
                <!-- Creditor (beneficiary) information -->
            </Cdtr>
            <CdtrAcct>
                <!-- Creditor account information -->
            </CdtrAcct>
        </CdtTrfTxInf>
    </FIToFICstmrCdtTrf>
</Document>
```

## Fedwire Envelope

When wrapping ISO 20022 messages for Fedwire, the library adds a Fedwire-specific envelope around the ISO 20022 XML:

```xml
<FedwireFundsOutgoing xmlns="urn:fedwirefunds:outgoing:v001">
    <FedwireFundsOutgoingMessage>
        <FedwireFundsCustomerCreditTransfer>
            <!-- AppHdr and Document elements from ISO 20022 -->
        </FedwireFundsCustomerCreditTransfer>
    </FedwireFundsOutgoingMessage>
</FedwireFundsOutgoing>
```

## Code Example

Here's a simplified example of how the code generation process works:

```python
from iso20022gen import Iso20022CodeGen

# Initialize the generator
generator = Iso20022CodeGen()

# Process the input data
payment_data = {
    "fedWireMessage": {
        # Payment details...
    }
}

# Generate the ISO 20022 message
result = generator.process(payment_data)

if result["statusCode"] == 200:
    iso_message = result["body"]
    print(iso_message)
```

## Debugging and Troubleshooting

If message generation fails, the library returns an error response with a statusCode other than 200 and an error message in the body. Common issues include:

1. **Missing Required Fields**: Ensure all required fields are provided in the input JSON.

2. **Invalid Data Format**: Check that data is in the correct format (e.g., dates in the right format).

3. **Schema Validation Errors**: If validation against XSD schemas fails, check that the generated XML conforms to ISO 20022 standards.

4. **XML Parsing Errors**: If wrapping in a Fedwire envelope fails, check that the ISO 20022 XML is well-formed. 