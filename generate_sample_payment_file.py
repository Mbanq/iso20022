    #!/usr/bin/env python3
"""
Generate a sample ISO20022 payment file using the dictionary-based approach.
"""

import json
from datetime import datetime, timezone
from uuid import uuid4

from iso20022gen.models import AppHdr, Document, model_to_xml


def main():
    # Load payload
    with open("iso20022gen/sample_files/sample_payment.json", "r") as f:
        payload = json.load(f)

    # Create model objects and convert to dict representation
    apphdr = AppHdr.from_payload(payload)
    document = Document.from_payload(payload)

    # Convert to XML
    apphdr_xml = model_to_xml(apphdr, "head", "urn:iso:std:iso:20022:tech:xsd:head.001.001.03")
    document_xml = model_to_xml(document, "pacs", "urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08")

    print("Generated XML files:\n")
    print("AppHdr XML:")
    print(apphdr_xml)
    print("\nDocument XML:")
    print(document_xml)

    # Combine both XMLs into a single file
    combined_xml = f"{apphdr_xml}\n{document_xml}"
    with open("output.xml", "w") as f:
        f.write(combined_xml)
    print("\nCombined XML saved to output.xml")

if __name__ == "__main__":
    main()
