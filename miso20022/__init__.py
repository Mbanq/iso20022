# SPDX-License-Identifier: Apache-2.0

"""
ISO 20022 data models package.
"""

from dataclasses import asdict
from miso20022.bah.apphdr import AppHdr
from miso20022.pacs import Document, FIToFICstmrCdtTrf
from miso20022.helpers import dict_to_xml, parse_xml_to_json
from miso20022.fedwire import (
    generate_fedwire_message,
    generate_fedwire_payload,
    parse_message_envelope,
    generate_message_structure,
)

def model_to_xml(model, prefix=None, namespace=None):
    """Convert model to XML using the dictionary-based approach."""
    if hasattr(model, 'to_dict'):
        xml_dict = model.to_dict()
    else:
        xml_dict = asdict(model)
        if prefix and namespace:
            xml_dict = {
                "Document": {
                    f"@xmlns:{prefix}": namespace,
                    **xml_dict
                }
            }
    return dict_to_xml(xml_dict, prefix=prefix, namespace=namespace)


__all__ = [
    "AppHdr",
    "Document",
    "FIToFICstmrCdtTrf",
    "dict_to_xml",
    "model_to_xml",
    "generate_fedwire_message",
    "generate_fedwire_payload",
    "parse_message_envelope",
    "generate_message_structure",
    "parse_xml_to_json",
]
