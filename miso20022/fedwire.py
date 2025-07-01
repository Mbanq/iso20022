# SPDX-License-Identifier: Apache-2.0

import sys
import re
import json
import xml.etree.ElementTree as ET
from typing import Dict, Any, Tuple, Optional, List, Union
from datetime import datetime

# Fix imports to use the correct package structure
from miso20022.bah.apphdr import AppHdr
from miso20022.pacs.pacs008 import Document as Pacs008Document 
from miso20022.pacs.pacs028 import Document as Pacs028Document
from miso20022.pacs.pacs002 import FIToFIPmtStsRpt
from miso20022.pacs.pacs008 import FIToFICstmrCdtTrf
from miso20022.helpers import dict_to_xml
from miso20022.helpers import parse_xml_to_json

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
    """
    # Check if message_code is provided
    if not message_code:
        raise ValueError("message_code parameter is required")
    
    # Define the namespaces
    namespaces = { 
        'xs': 'http://www.w3.org/2001/XMLSchema'
    }
    
    # Parse the XSD file
    try:
        # Read the file content directly to extract namespace declarations
        with open(xsd_path, 'r') as file:
            content = file.read()
            
        # Extract namespace declarations using regex
        ns_mapping = {}
        ns_pattern = r'xmlns:([a-zA-Z0-9]+)="([^"]+)"'
        for match in re.finditer(ns_pattern, content):
            prefix, uri = match.groups()
            ns_mapping[prefix] = uri
            
        # Now parse the file with ElementTree
        tree = ET.parse(xsd_path)
        root = tree.getroot()
    except Exception as e:
        print(f"Error parsing XSD file: {e}")
        sys.exit(1)
    
    # Extract the target namespace
    target_ns = root.get('targetNamespace')
    if not target_ns:
        print("Error: XSD file does not have a target namespace.")
        sys.exit(1)
        
    # Add the target namespace to our namespaces dictionary
    namespaces['tns'] = target_ns
    
    # Find the root element and message container element
    root_elements = []
    for element in root.findall('.//xs:element', namespaces):
        name = element.get('name')
        if name:
            root_elements.append(name)
    
    # Determine the root element (usually the first one defined)
    root_element_name = root_elements[0] if root_elements else None
    
    # Determine the message container element (usually the second one defined)
    message_container_name = root_elements[2] if len(root_elements) > 2 else (root_elements[1] if len(root_elements) > 1 else None)
    
    # Find all elements that could be message types
    for element in root.findall('.//xs:element', namespaces):
        name = element.get('name')
        # Skip the root elements and technical headers
        if (name and 
            name != root_element_name and 
            name != message_container_name and
            not name.endswith('TechnicalHeader')):
            
            # Check if this element has child elements that include Document
            has_document = False
            for seq in element.findall('.//xs:sequence', namespaces):
                for child in seq.findall('.//xs:element', namespaces):
                    ref = child.get('ref')
                    if ref and 'Document' in ref:
                        has_document = True
                        break
            
            if has_document:
                # This is a message type element
                
                # Find the child elements to determine which message code it uses
                for seq in element.findall('.//xs:sequence', namespaces):
                    for child in seq.findall('.//xs:element', namespaces):
                        ref = child.get('ref')
                        if ref:
                            try:
                                prefix, local_name = ref.split(':')
                                if prefix in ns_mapping:
                                    namespace = ns_mapping[prefix]
                                    if local_name == 'Document':
                                        # Extract the message code from the namespace
                                        current_message_code = namespace
                                        
                                        # If we found the requested message code, return the data
                                        if current_message_code == message_code:
                                            return name, target_ns, root_element_name, message_container_name
                            except ValueError:
                                # Skip refs that don't have a prefix
                                continue
    
    # If we've gone through all elements and haven't found the message code, raise an error
    raise ValueError(f"Message code '{message_code}' not found in the XSD file.")

def generate_message_structure(app_hdr_xml, document_xml, name, target_ns, root_element_name, message_container_name):
    """
    Generate the message structure for a given message code.
    
    Args:
        app_hdr_xml: The AppHdr XML
        document_xml: The Document XML
        name: The element name
        target_ns: The target namespace
        root_element_name: The root element name
        message_container_name: The message container name
        
    Returns:
        The XML structure as a string
    """
    # Create the XML structure
    app_hdr_lines = app_hdr_xml.strip().split('\n')
    document_lines = document_xml.strip().split('\n')
    
    # Indent the lines properly
    app_hdr_indented = '\n        '.join(app_hdr_lines)
    document_indented = '\n        '.join(document_lines)
    
    complete_structure = f"""<{root_element_name} xmlns="{target_ns}">
  <{message_container_name}>
    <{name}>
        {app_hdr_indented}
        {document_indented}
    </{name}>
  </{message_container_name}>
</{root_element_name}>"""
    
    return complete_structure

def generate_fedwire_message(message_code: str, environment: str, fed_aba: str, payload: Dict[str, Any], xsd_path: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Generate a complete ISO20022 message using the models from miso20022.
    
    Args:
        message_code: The ISO20022 message code (e.g., urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08).
        environment: The environment for the message, either "TEST" or "PROD".
        fed_aba: The Fed ABA number for message generation.
        payload: The payload data as a dictionary.
        xsd_path: Path to the XSD file for structure identification.
        
    Returns:
        Tuple of (AppHdr XML, Document XML, Complete Structure XML) or (None, None, None) if not supported.
    """
    # Extract the message type from the message code
    message_type = message_code.split(':')[-1]
    
    try:
        # Generate AppHdr
        app_hdr = AppHdr.from_payload(environment, fed_aba, message_code, payload)
        app_hdr_dict = app_hdr.to_dict()
        app_hdr_xml = dict_to_xml(app_hdr_dict, "head", "urn:iso:std:iso:20022:tech:xsd:head.001.001.03")
        
        # Generate Document based on message type
        document_xml = None
        
        # Only support pacs.008 and pacs.028 message types
        if "pacs.008" in message_type:
            try:
                # Use the specific model for pacs.008
                document = Pacs008Document.from_payload(payload)
                document_dict = document.to_dict()
                document_xml = dict_to_xml(document_dict, "pacs", message_code)
            except Exception as e:
                print(f"Error generating pacs.008 structure: {e}")
                return None, None, None
                
        elif "pacs.028" in message_type:
            try:
                document = Pacs028Document.from_payload(payload)
                document_dict = document.to_dict()
                document_xml = dict_to_xml(document_dict, "pacs", message_code)
                print(f"Generated structure for pacs.028 message type using model")
            except Exception as e:
                print(f"Error generating pacs.028 structure: {e}")
                print("Make sure you're providing the correct payload structure for pacs.028")
                return None, None, None
        else:
            # All other message types are unsupported
            print(f"Message type {message_type} is not currently supported for generation.")
            return None, None, None
        
        # Generate the complete structure
        complete_structure = None
        try:
            # Get the specific message data - use full message_code, not just message_type
            element_name, target_ns, root_element_name, message_container_name = parse_message_envelope(xsd_path, message_code)
            
            # Create the complete XML structure with the actual generated content
            app_hdr_lines = app_hdr_xml.strip().split('\n')
            document_lines = document_xml.strip().split('\n')
            
            # Indent the lines properly
            app_hdr_indented = '\n        '.join(app_hdr_lines)
            document_indented = '\n        '.join(document_lines)
            
            complete_structure = f"""<{root_element_name} xmlns="{target_ns}">
  <{message_container_name}>
    <{element_name}>
        {app_hdr_indented}
        {document_indented}
    </{element_name}>
  </{message_container_name}>
</{root_element_name}>"""
        except ValueError as e:
            print(f"Error generating complete structure: {e}")
            return None, None, None
        
        return app_hdr_xml, document_xml, complete_structure
        
    except Exception as e:
        print(f"Error generating message: {e}")
        return None, None, None

def get_account_number(Acct):
    """Safely retrieves the account number from an Acct object."""
    if not Acct or not hasattr(Acct, 'Id') or not Acct.Id:
        return ""
    # Prioritize Other ID if available
    if hasattr(Acct.Id.Othr, 'Id') and Acct.Id.Othr.Id:
        return Acct.Id.Othr.Id

    # Fallback to IBAN
    if hasattr(Acct.Id, 'IBAN') and Acct.Id.IBAN:
        return Acct.Id.IBAN

    return ""

def pacs_008_to_fedwire_json    (app_hdr, cdt_trf_tx_inf, grp_hdr_data):
    """Maps AppHdr and CdtTrfTxInf data classes to the Fedwire JSON format. Supports PACS008 Only"""

    # Helper to safely extract address lines
    def get_adr_line(pstl_adr, index):
        if not pstl_adr:
            return ""

        constructed_line = ""
        
        if index == 0:  # Line 1: Street Name and Building Number
            line_parts = filter(None, [pstl_adr.StrtNm, pstl_adr.BldgNb])
            constructed_line = " ".join(line_parts).strip()
        elif index == 1:  # Line 2: Floor and Room
            flr_part = f"Flr {pstl_adr.Flr}" if pstl_adr.Flr else None
            room_part = pstl_adr.Room
            line_parts = filter(None, [flr_part, room_part])
            constructed_line = ", ".join(line_parts).strip()
        elif index == 2:  # Line 3: Town, State/Province PostalCode, Country
            town_part = pstl_adr.TwnNm
            # Combine State/Province and Postal Code, e.g., "CA 90210" or "CA" or "90210"
            state_zip_part = " ".join(filter(None, [pstl_adr.CtrySubDvsn, pstl_adr.PstCd])).strip()
            country_part = pstl_adr.Ctry
            
            # Combine all parts of Line 3 with commas, filtering out empty ones
            all_line3_parts = filter(None, [town_part, state_zip_part, country_part])
            constructed_line = ", ".join(all_line3_parts).strip()
        
        # Return the constructed line if not empty, otherwise fallback to AdrLine
        if constructed_line:
            return constructed_line
        elif pstl_adr.AdrLine and len(pstl_adr.AdrLine) > index and pstl_adr.AdrLine[index]:
            return pstl_adr.AdrLine[index] # Return AdrLine if it's not empty
        else:
            return ""

    fedwire_message = {
        "fedWireMessage": {
            "inputMessageAccountabilityData": {
                "inputCycleDate": grp_hdr_data.MsgId[:8],
                "inputSource": grp_hdr_data.MsgId[8:13],
                "inputSequenceNumber": grp_hdr_data.MsgId[13:]
            },
            "amount": {
                "amount": str(int(float(cdt_trf_tx_inf.IntrBkSttlmAmt['#text'])))
            },
            "senderDepositoryInstitution": {
                "senderABANumber": cdt_trf_tx_inf.InstgAgt.FinInstnId.ClrSysMmbId.MmbId,
                "senderShortName": cdt_trf_tx_inf.DbtrAgt.FinInstnId.Nm or ""
            },
            "receiverDepositoryInstitution": {
                "receiverABANumber": cdt_trf_tx_inf.InstdAgt.FinInstnId.ClrSysMmbId.MmbId,
                "receiverShortName": cdt_trf_tx_inf.CdtrAgt.FinInstnId.Nm or ""
            },
            "originator": {
                "personal": {
                    "name": cdt_trf_tx_inf.Dbtr.Nm,
                    "address": {
                        "addressLineOne": get_adr_line(cdt_trf_tx_inf.Dbtr.PstlAdr, 0),
                        "addressLineTwo": get_adr_line(cdt_trf_tx_inf.Dbtr.PstlAdr, 1),
                        "addressLineThree": get_adr_line(cdt_trf_tx_inf.Dbtr.PstlAdr, 2)
                    },
                    "identifier": get_account_number(cdt_trf_tx_inf.DbtrAcct)
                }
            },
            "beneficiary": {
                "personal": {
                    "name": cdt_trf_tx_inf.Cdtr.Nm,
                    "address": {
                        "addressLineOne": get_adr_line(cdt_trf_tx_inf.Cdtr.PstlAdr, 0),
                        "addressLineTwo": get_adr_line(cdt_trf_tx_inf.Cdtr.PstlAdr, 1),
                        "addressLineThree": get_adr_line(cdt_trf_tx_inf.Cdtr.PstlAdr, 2)
                    },
                    "identifier": get_account_number(cdt_trf_tx_inf.CdtrAcct)
                }
            }
        }
    }
    return fedwire_message


def pacs_002_to_fedwire_json(app_hdr, pmt_sts_req):
    """Maps AppHdr and FIToFIPmtStsRpt data classes to the Fedwire JSON format."""

    #TODO: Add status and reason
    fedwire_message = {
        "fedWireMessage": {
            "inputMessageAccountabilityData": {
                "inputCycleDate": pmt_sts_req.TxInfAndSts.OrgnlGrpInf['OrgnlMsgId'][:8],
                "inputSource": pmt_sts_req.TxInfAndSts.OrgnlGrpInf['OrgnlMsgId'][8:13],
                "inputSequenceNumber": pmt_sts_req.TxInfAndSts.OrgnlGrpInf['OrgnlMsgId'][13:]
            },
            "outputMessageAccountabilityData": {
                "outputCycleDate": pmt_sts_req.GrpHdr.MsgId[:8],
                "outputSource": pmt_sts_req.GrpHdr.MsgId[8:13],
                "outputSequenceNumber": pmt_sts_req.GrpHdr.MsgId[13:]
            }
        }
    }
    return fedwire_message
    

def generate_fedwire_payload(xml_file, message_code):

    # 1. Parse the XML file to JSON
    json_output = parse_xml_to_json(xml_file)
    data = json.loads(json_output)

    # 2. Instantiate the AppHdr & CdtTrfTxInf data class
    
    if message_code == "urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08":

        app_hdr_instance = AppHdr.from_iso20022(data,message_code)
        grp_hdr_data, cdt_trf_tx_inf = FIToFICstmrCdtTrf.from_iso20022(data)

        # 3. Map to Fedwire JSON format
        fedwire_json = pacs_008_to_fedwire_json(app_hdr_instance, cdt_trf_tx_inf, grp_hdr_data)

    elif message_code == "urn:iso:std:iso:20022:tech:xsd:pacs.002.001.10":

        app_hdr_instance = AppHdr.from_iso20022(data,message_code)
        pmt_sts_req= FIToFIPmtStsRpt.from_iso20022(data)
        
        # 3. Map to Fedwire JSON format
        fedwire_json = pacs_002_to_fedwire_json(app_hdr_instance, pmt_sts_req)

    else:
        raise ValueError(f"Unsupported message code: {message_code}")
    
    return fedwire_json
