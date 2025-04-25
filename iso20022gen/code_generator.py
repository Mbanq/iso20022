"""
Core ISO 20022 code generation functionality.
"""
import json
import logging
import os
import sys
from json import dumps
from typing import Dict, Any, Tuple, Optional

import xmlschema

from iso20022gen import config
from iso20022gen.models import model_to_xml, xml_converter
from iso20022gen.models.apphdr import AppHdr
from iso20022gen.models.pacs008 import Document

logger = logging.getLogger(__name__)


class Iso20022CodeGen:

    def __init__(self, schemas_path: Optional[str] = None) -> None:

        self.schemas_path = schemas_path or config.XSD_PATH

    def generate_iso20022_apphdr_and_pacs008(self, payload: Dict[str, Any]) -> Tuple[str, str]:
        # Create model objects from payload
        app_hdr = AppHdr.from_payload(payload)
        document = Document.from_payload(payload)

        # Convert dictionaries to XML
        # apphdr_xml = model_to_xml(app_hdr)
        document_xml = model_to_xml(document, 'urn2', 'urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08')

        return apphdr_xml, document_xml

    def create_iso2022_pacs_002(self, payload: Dict[str, Any], direction: str = "") -> Tuple[str, str]:
        # This is a placeholder for future implementation
        # Will be implemented in a future version
        logger.warning("pacs.002 message generation not yet implemented")
        return "", ""

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:

        try:
            apphdr_xml, document_xml = self.generate_iso20022_apphdr_and_pacs008(payload)
            schema_apphdr_path = os.path.join(self.schemas_path, "head.001.001.03.xsd")
            schema_pacs008_path = os.path.join(self.schemas_path, "pacs.008.001.08.xsd")

            if os.path.exists(schema_apphdr_path) and os.path.exists(schema_pacs008_path):
                schema_apphdr = xmlschema.XMLSchema(schema_apphdr_path)
                schema_pacs008 = xmlschema.XMLSchema(schema_pacs008_path)

                try:
                    schema_apphdr.validate(apphdr_xml)
                    schema_pacs008.validate(document_xml)
                except xmlschema.XMLSchemaValidationError as e:
                    logger.error(f"Validation error: {e}")
                    return {
                        "statusCode": 400,
                        "headers": {"Content-Type": "application/json"},
                        "body": dumps({"error": f"XML validation failed: {str(e)}"})
                    }
            else:
                logger.warning("Schema files not found, skipping validation")

            xml_pacs = xml_converter.combine_xml_documents(apphdr_xml, document_xml)

            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/xml"},
                "body": xml_pacs
            }

        except KeyError as e:
            error_message = f"Missing required field in input data: {e}"
            logger.error(error_message)
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": dumps({"error": error_message})
            }
        except Exception as e:
            error_message = f"Error processing ISO 20022 message: {e}"
            logger.error(error_message)
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": dumps({"error": error_message})
            }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python iso_20022_outgoing_fedwire.py <payload.json>")
        sys.exit(1)

    payload_file = sys.argv[1]
    with open(payload_file, "r") as f:
        payload = json.load(f)

    # Using the Iso20022CodeGen class from iso20022gen package
    processor = Iso20022CodeGen()
    result = processor.process(payload)

    if result["statusCode"] == 200:
        result_xml = result["body"]
        print("Generated XML:")
        print(result_xml)
