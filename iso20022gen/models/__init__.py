"""
ISO 20022 data models package.
"""

from dataclasses import asdict
from iso20022gen.models.bah.apphdr import AppHdr
from iso20022gen.models.pacs import Document, FIToFICstmrCdtTrf
from iso20022gen.models.helpers import dict_to_xml

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
