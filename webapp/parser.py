# SPDX-License-Identifier: Apache-2.0

import xml.etree.ElementTree as ET
from typing import Dict, Any
import tempfile
import os
import json
from miso20022.fedwire import generate_fedwire_payload

def parse_xml_message(xml_content: str, message_code: str) -> Dict[str, Any]:
    """
    Parses an ISO20022 XML message using the `generate_fedwire_payload` function,
    which requires writing the content to a temporary file.
    """
    temp_file_path = None
    try:
        # `generate_fedwire_payload` requires a file path.
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.xml', encoding='utf-8') as temp_file:
            temp_file.write(xml_content)
            temp_file_path = temp_file.name

        # Call the fedwire parser
        document_payload = generate_fedwire_payload(temp_file_path, message_code)
        if not document_payload:
            raise ValueError("Failed to parse document payload. Check if the message code is correct or if the XML is valid for this message type.")

        return document_payload
    except Exception as e:
        # Re-raise exceptions to be caught by the app
        raise e
    finally:
        # Clean up the temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
