"""
Utility to convert dictionaries to XML format.
"""
from typing import Any, Dict, List, Union, Optional
import xmltodict


def dict_to_xml(data: Union[Dict[str, Any], List[Any]], prefix, namespace, root: Optional[str] = None) -> str:
    """
    Convert a dictionary to an XML string with optional namespace prefix.

    Args:
        data: Dictionary or list to convert.
        prefix: Namespace prefix to apply to element tags.
        namespace: Namespace URI to declare on the root element.
        root: Optional root element name to wrap data.

    Returns:
        Namespaced XML string.
    """
    # If the caller provided a `root` name, wrap everything under it:
    if root:
        data = {root: data}

    def _apply_prefix(obj):
        if isinstance(obj, dict):
            new_obj = {}
            for key, value in obj.items():
                # Don’t prefix attributes or the text node
                if key.startswith('@') or key == '#text':
                    new_obj[key] = _apply_prefix(value)
                else:
                    prefixed_key = f"{prefix}:{key}"
                    new_obj[prefixed_key] = _apply_prefix(value)
            return new_obj
        elif isinstance(obj, list):
            return [_apply_prefix(item) for item in obj]
        else:
            return obj

    # Apply prefix to all tags
    if prefix and namespace:
        data = _apply_prefix(data)

    # Wrap everything under the Document element with your prefix
    doc_key = f"{prefix}:Document"
    data = {doc_key: data}

    # Declare namespace on the Document element
    data[doc_key]["@xmlns:" + prefix] = namespace

    # Generate XML without the XML declaration
    return xmltodict.unparse(data, pretty=True, full_document=False)
