"""
ISO 20022 data models package.
"""

# Import the dictionary-based implementations instead of Pydantic models
from iso20022gen.models.xml_converter import dict_to_xml


def model_to_xml(model, prefix, namespace):
    """Convert model to XML using the dictionary-based approach."""
    if hasattr(model, 'to_dict'):
        xml_dict = model.to_dict()
        return dict_to_xml(xml_dict, prefix, namespace)
    return dict_to_xml(model)
