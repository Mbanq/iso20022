# SPDX-License-Identifier: Apache-2.0

"""
Utility to convert dictionaries to XML format.
"""
from typing import Any, Dict, List, Union, Optional
import xmltodict
from lxml import etree
import json

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

def parse_xml_to_json(xml_file_path: str) -> str:
    """Parses an XML file and converts it to a JSON string."""
    try:
        tree = etree.parse(xml_file_path)
        root = tree.getroot()

        def element_to_dict(element):
            """Recursively converts an lxml element to a dictionary."""
            # Remove namespace from tag name
            tag = etree.QName(element).localname

            node_dict = {}

            # Add attributes to the dictionary
            if element.attrib:
                node_dict['@attributes'] = {k: v for k, v in element.attrib.items()}

            # Add child elements to the dictionary
            children = element.getchildren()
            if children:
                for child in children:
                    child_tag, child_data = element_to_dict(child).popitem()
                    if child_tag in node_dict:
                        if not isinstance(node_dict[child_tag], list):
                            node_dict[child_tag] = [node_dict[child_tag]]
                        node_dict[child_tag].append(child_data)
                    else:
                        node_dict[child_tag] = child_data

            # Add text content to the dictionary
            if element.text and element.text.strip():
                text = element.text.strip()
                if node_dict:  # If there are attributes or children, add text as a key
                    node_dict['#text'] = text
                else:  # Otherwise, the element's value is just the text
                    node_dict = text

            return {tag: node_dict}

        xml_dict = element_to_dict(root)
        return json.dumps(xml_dict, indent=4)

    except etree.XMLSyntaxError as e:
        raise ValueError(f"Error parsing XML file: {e}")
    except Exception as e:
        raise IOError(f"Error reading file or processing XML: {e}")
