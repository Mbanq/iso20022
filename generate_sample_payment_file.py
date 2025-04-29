#!/usr/bin/env python3
"""
Test the ISO 20022 message generation using the available models.
"""
import json
from dataclasses import asdict
from iso20022gen.models.apphdr import AppHdr
from iso20022gen.models.pacs008 import Document
from iso20022gen.models.xml_converter import dict_to_xml

def main():
    # Load payload
    with open("iso20022gen/examples/sample_payment.json", "r") as f:
        payload = json.load(f)

    # Create model objects and convert to dict representation
    app_hdr = AppHdr.from_payload(payload)
    app_hdr_dict = asdict(app_hdr)

    document = Document.from_payload(payload)
    document_dict = asdict(document)

    # Convert to XML with proper namespaces
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

    print("Generated XML files:")
    print("\nAppHdr XML:")
    print(app_hdr_xml)
    print("\nDocument XML:")
    print(document_xml)
    print("\nCombined XML saved to output.xml")

if __name__ == "__main__":
    main()
