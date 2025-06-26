#!/usr/bin/env python3
"""
Validate ISO20022 XML files against their XSD schemas.
"""

import sys
import re
from lxml import etree


def extract_document_xml(xml_file):
    """Extract the Document XML from a file containing both AppHdr and Document."""
    with open(xml_file, 'r') as f:
        content = f.read()

    # Find Document tag
    match = re.search(r'<(?:\w+:)?Document[^>]*>.*?</(?:\w+:)?Document>', content, re.DOTALL)
    if match:
        return match.group(0)
    else:
        raise ValueError(f"Could not find Document XML in {xml_file}")


def extract_apphdr_xml(xml_file):
    """Extract the AppHdr XML from a file containing both AppHdr and Document."""
    with open(xml_file, 'r') as f:
        content = f.read()

    # Find AppHdr tag
    match = re.search(r'<(?:\w+:)?AppHdr[^>]*>.*?</(?:\w+:)?AppHdr>', content, re.DOTALL)
    if match:
        return match.group(0)
    else:
        raise ValueError(f"Could not find AppHdr XML in {xml_file}")


def validate_xml(xml_content, xsd_file):
    """Validate XML content against an XSD schema."""
    try:
        xmlschema_doc = etree.parse(xsd_file)
        xmlschema = etree.XMLSchema(xmlschema_doc)
        
        # Parse the XML content
        xml_doc = etree.fromstring(xml_content.encode('utf-8'))
        
        # Validate against the schema
        is_valid = xmlschema.validate(xml_doc)
        
        if is_valid:
            print("✅ XML is valid according to schema!")
            return True
        else:
            print("❌ XML is invalid according to schema!")
            print("Validation errors:")
            for error in xmlschema.error_log:
                print(f"  Line {error.line}: {error.message}")
            return False

    except etree.XMLSyntaxError as e:
        print("❌ XML syntax error:")
        for error in e.error_log:
            print(f"  Line {error.line}: {error.message}")
        return False

    except Exception as e:
        print(f"Error during validation: {str(e)}")
        return False


def detect_message_type(xml_file):
    """Detect the message type from the XML file."""
    with open(xml_file, 'r') as f:
        content = f.read()
    
    # Check for pacs.028
    if 'pacs.028.001.03' in content:
        return 'pacs.028'
    # Check for pacs.008
    elif 'pacs.008.001.08' in content:
        return 'pacs.008'
    else:
        return None


if __name__ == "__main__":
    # Get the XML file to validate
    if len(sys.argv) > 1:
        xml_file = sys.argv[1]
    else:
        xml_file = "output.xml"
    
    # Define XSD schemas
    apphdr_xsd = "mb_iso20022/schemas/head.001.001.03.xsd"
    pacs008_xsd = "mb_iso20022/schemas/pacs.008.001.08.xsd"
    pacs028_xsd = "mb_iso20022/schemas/pacs.028.001.03.xsd"
    
    # Detect message type
    message_type = detect_message_type(xml_file)
    
    # Validate AppHdr
    print("Validating AppHdr...")
    try:
        apphdr_xml = extract_apphdr_xml(xml_file)
        validate_xml(apphdr_xml, apphdr_xsd)
    except Exception as e:
        print(f"Error validating AppHdr: {str(e)}")
    
    # Validate Document based on message type
    if message_type == 'pacs.008':
        print("\nValidating PACS.008 Document...")
        try:
            document_xml = extract_document_xml(xml_file)
            validate_xml(document_xml, pacs008_xsd)
        except Exception as e:
            print(f"Error validating PACS.008: {str(e)}")
    
    elif message_type == 'pacs.028':
        print("\nValidating PACS.028 Document...")
        try:
            document_xml = extract_document_xml(xml_file)
            validate_xml(document_xml, pacs028_xsd)
        except Exception as e:
            print(f"Error validating PACS.028: {str(e)}")
    
    else:
        print("\nUnknown message type. Please specify a valid ISO20022 message type.")
