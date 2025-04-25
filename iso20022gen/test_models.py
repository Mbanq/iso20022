"""
Test script for ISO 20022 model-based XML generation.
"""
import json
import sys
from iso20022gen.models.dict_models import AppHdr, Document
from iso20022gen.models.xml_converter import dict_to_xml, combine_xml_documents


def test_models(payload_file):
    """Test the models with a sample payload."""
    # Load the payload from file
    with open(payload_file, "r") as f:
        payload = json.load(f)
    
    # Create model objects
    app_hdr = AppHdr.from_payload(payload)
    document = Document.from_payload(payload)
    
    # Convert models to dictionary representation
    app_hdr_dict = app_hdr.to_dict()
    document_dict = document.to_dict()
    
    # Convert dictionaries to XML
    app_hdr_xml = dict_to_xml(app_hdr_dict)
    document_xml = dict_to_xml(document_dict)
    
    # Print the XML
    print("AppHdr XML:")
    print(app_hdr_xml)
    print("\nDocument XML:")
    print(document_xml)
    
    # Combined XML
    combined_xml = combine_xml_documents(app_hdr_xml, document_xml)
    
    # Save to file
    with open("output.xml", "w") as f:
        f.write(combined_xml)
    
    print("\nCombined XML saved to output.xml")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m iso20022gen.test_models <payload.json>")
        sys.exit(1)
    
    payload_file = sys.argv[1]
    test_models(payload_file) 