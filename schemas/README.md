# ISO 20022 Schemas

This directory should contain ISO 20022 XSD schema files used for validation.

## Required Schema Files

The following schema files are required for basic functionality:

- `head.001.001.03.xsd`: ISO 20022 AppHdr schema
- `pacs.008.001.08.xsd`: ISO 20022 Customer Credit Transfer schema

## How to Obtain Schemas

The schema files can be downloaded from the ISO 20022 website at [www.iso20022.org](https://www.iso20022.org).

1. Visit the ISO 20022 website
2. Navigate to the "Catalogue of Messages" section
3. Download the required XSD files
4. Place them in this directory

## Validation

The schemas are used to validate the generated ISO 20022 messages before they are sent to ensure compliance with the standard. 