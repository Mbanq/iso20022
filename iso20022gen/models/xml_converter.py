"""
Utility to convert dictionaries to XML format.
"""
from typing import Any, Dict, List, Union, Optional
import xmltodict


def _remove_none_values(obj):
    """Remove None values from a dictionary recursively."""
    if isinstance(obj, dict):
        return {k: _remove_none_values(v) for k, v in obj.items() if v is not None}
    elif isinstance(obj, list):
        return [_remove_none_values(item) for item in obj]
    return obj


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
    # Remove None values first
    data = _remove_none_values(data)

    def _apply_prefix(obj):
        if isinstance(obj, dict):
            new_obj = {}
            for key, value in obj.items():
                # Don't prefix attributes or the text node
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

    # If root is provided, wrap the data in it
    if root:
        root_key = f"{prefix}:{root}"
        data = {root_key: data}
        # Declare namespace on the root element
        data[root_key]["@xmlns:" + prefix] = namespace

    # Generate XML without the XML declaration
    return xmltodict.unparse(data, pretty=True, full_document=False)
