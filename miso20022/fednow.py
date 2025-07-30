# SPDX-License-Identifier: Apache-2.0

import sys
import re
import xml.etree.ElementTree as ET
from typing import Dict, Any, Tuple, Optional

# Fix imports to use the correct package structure
from miso20022.bah.apphdr import AppHdr
from miso20022.admi.admi004 import Admi004Document
from miso20022.helpers import dict_to_xml

def parse_message_envelope(xsd_path, message_code):
    """
    Parse the XSD file and return data for a specific message code.
    
    Args:
        xsd_path: Path to the XSD file
        message_code: The specific message code to return data for (required)
        
    Returns:
        A tuple containing (element_name, target_ns, root_element_name, message_container_name) for the specified message code
        
    Raises:
        ValueError: If message_code is not provided or not found in the XSD file
        IOError: If the XSD file cannot be parsed
    """
    if not message_code:
        raise ValueError("message_code parameter is required")
    
    namespaces = {'xs': 'http://www.w3.org/2001/XMLSchema'}
    
    try:
        with open(xsd_path, 'r') as file:
            content = file.read()
            
        ns_mapping = {}
        ns_pattern = r'xmlns:([a-zA-Z0-9]+)=\"([^\"]+)\"'
        for match in re.finditer(ns_pattern, content):
            prefix, uri = match.groups()
            ns_mapping[prefix] = uri
            
        tree = ET.parse(xsd_path)
        root = tree.getroot()
    except Exception as e:
        raise IOError(f"Error parsing XSD file: {e}")
    
    target_ns = root.get('targetNamespace')
    if not target_ns:
        raise ValueError("XSD file does not have a target namespace.")
        
    namespaces['tns'] = target_ns
    
    root_elements = [elem.get('name') for elem in root.findall('.//xs:element', namespaces) if elem.get('name')]
    
    root_element_name = root_elements[0] if root_elements else None
    message_container_name = root_elements[2] if len(root_elements) > 2 else (root_elements[1] if len(root_elements) > 1 else None)
    
    for element in root.findall('.//xs:element', namespaces):
        name = element.get('name')
        if not (name and name != root_element_name and name != message_container_name and not name.endswith('TechnicalHeader')):
            continue

        has_document = any('Document' in child.get('ref', '') for seq in element.findall('.//xs:sequence', namespaces) for child in seq.findall('.//xs:element', namespaces))
        
        if has_document:
            for seq in element.findall('.//xs:sequence', namespaces):
                for child in seq.findall('.//xs:element', namespaces):
                    ref = child.get('ref')
                    if ref and ':' in ref:
                        prefix, local_name = ref.split(':', 1)
                        if prefix in ns_mapping and local_name == 'Document':
                            current_message_code = ns_mapping[prefix]
                            if current_message_code == message_code:
                                return name, target_ns, root_element_name, message_container_name
    
    raise ValueError(f"Message code '{message_code}' not found in the XSD file.")

def generate_message_structure(app_hdr_xml, document_xml, name, target_ns, root_element_name, message_container_name):
    """
    Generate the message structure for a given message code.
    """
    app_hdr_indented = '\n        '.join(app_hdr_xml.strip().split('\n'))
    document_indented = '\n        '.join(document_xml.strip().split('\n'))
    
    return f"""<{root_element_name} xmlns="{target_ns}">
  <{message_container_name}>
    <{name}>
        {app_hdr_indented}
        {document_indented}
    </{name}>
  </{message_container_name}>
</{root_element_name}>"""

def generate_fednow_message(message_code: str, environment: str, fed_aba: str, payload: Dict[str, Any], xsd_path: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Generate a complete ISO20022 message for FedNow, supporting admi.004.
    
    Args:
        message_code: The ISO20022 message code (e.g., urn:iso:std:iso:20022:tech:xsd:admi.004.001.02).
        environment: The environment for the message, either "TEST" or "PROD".
        fed_aba: The Fed ABA number for message generation.
        payload: The payload data as a dictionary.
        xsd_path: Path to the XSD file for structure identification.
        
    Returns:
        Tuple of (AppHdr XML, Document XML, Complete Structure XML) or (None, None, None) if not supported.
    """
    message_type = message_code.split(':')[-1]

    try:
        # Generate AppHdr
        app_hdr = AppHdr.from_payload(environment, fed_aba, message_code, payload, payment_system='fednow')
        app_hdr_xml = dict_to_xml(app_hdr.to_dict(), "head", "urn:iso:std:iso:20022:tech:xsd:head.001.001.03")

        # Generate Document based on message type
        if "admi.004" in message_type:
            document = Admi004Document.from_payload(payload)
            document_dict = document.to_dict(message_code)
            document_xml = dict_to_xml(document_dict, None, message_code)
        else:
            print(f"Message type {message_type} is not currently supported for FedNow generation.")
            return None, None, None

        # Get the message envelope structure from the XSD
        element_name, target_ns, root_element_name, message_container_name = parse_message_envelope(xsd_path, message_code)
        
        # Generate the complete XML structure
        complete_structure = generate_message_structure(
            app_hdr_xml, document_xml, element_name, target_ns, root_element_name, message_container_name
        )
        
        return app_hdr_xml, document_xml, complete_structure
        
    except (ValueError, IOError) as e:
        print(f"Error generating FedNow message: {e}")
        return None, None, None
    except Exception as e:
        print(f"An unexpected error occurred during FedNow message generation: {e}")
        return None, None, None


