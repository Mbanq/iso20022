"""
Sample usage of the ISO20022 message generation using model-based approach.
"""
import json
import sys
from pathlib import Path

from iso20022gen.models.dict_models import AppHdr, Document
from iso20022gen.models.xml_converter import dict_to_xml, combine_xml_documents


def generate_iso20022_message(payload_file: str) -> str:
    """
    Generate an ISO20022 message from a FedWire payload.
    
    Args:
        payload_file: Path to the JSON payload file
        
    Returns:
        Combined XML string
    """
    # Load the payload
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
    
    # Combine XML documents
    combined_xml = combine_xml_documents(app_hdr_xml, document_xml)
    
    return combined_xml


def save_xml_to_file(xml_content: str, output_file: str) -> None:
    """
    Save XML content to a file.
    
    Args:
        xml_content: XML content
        output_file: Output file path
    """
    with open(output_file, "w") as f:
        f.write(xml_content)
    print(f"XML saved to {output_file}")


def main() -> None:
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python -m iso20022gen.sample_usage <payload.json> [output.xml]")
        sys.exit(1)
    
    payload_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "iso20022_output.xml"
    
    print(f"Generating ISO20022 message from {payload_file}...")
    xml_content = generate_iso20022_message(payload_file)
    
    # Save to file
    save_xml_to_file(xml_content, output_file)
    
    # Print summary
    print("\nGeneration Summary:")
    print(f"- Input: {payload_file}")
    print(f"- Output: {output_file}")
    print(f"- Size: {len(xml_content)} bytes")
    print("\nDone!")


if __name__ == "__main__":
    main() 