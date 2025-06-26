# SPDX-License-Identifier: Apache-2.0

"""
ISO 20022 data models package.
"""

from dataclasses import asdict
from miso20022.bah.apphdr import AppHdr
from miso20022.pacs import Document, FIToFICstmrCdtTrf
from miso20022.helpers import dict_to_xml

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
]
