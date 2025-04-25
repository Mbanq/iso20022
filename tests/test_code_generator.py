"""
Tests for the ISO 20022 Code Generator module.
"""
import json
import os
import pytest
from unittest.mock import patch, MagicMock

from iso20022gen import Iso20022CodeGen


@pytest.fixture
def sample_payload():
    """Provide a sample payload for testing."""
    return {
        "fedWireMessage": {
            "inputMessageAccountabilityData": {
                "inputCycleDate": "20250109",
                "inputSource": "TEST001",
                "inputSequenceNumber": "000001"
            },
            "amount": {
                "amount": "000000001000"
            },
            "senderDepositoryInstitution": {
                "senderABANumber": "121182904",
                "senderShortName": "TEST BANK"
            },
            "receiverDepositoryInstitution": {
                "receiverABANumber": "084106768",
                "receiverShortName": "RECEIVING BANK"
            },
            "beneficiary": {
                "personal": {
                    "identificationCode": "D",
                    "identifier": "9512227031535633",
                    "name": "JOHN DOE",
                    "address": {
                        "addressLineOne": "123 MAIN STREET",
                        "addressLineTwo": "ANYTOWN TX 12345"
                    }
                }
            },
            "originator": {
                "personal": {
                    "identificationCode": "D",
                    "identifier": "550103129900943",
                    "name": "JANE SMITH",
                    "address": {
                        "addressLineOne": "456 OAK AVENUE",
                        "addressLineTwo": "SOMEWHERE CA 67890",
                        "addressLineThree": ""
                    }
                }
            }
        }
    }


def test_generate_iso20022_apphdr_and_pacs008(sample_payload):
    """Test generating ISO 20022 AppHdr and Document XML."""
    # Initialize the generator
    generator = Iso20022CodeGen()
    
    # Generate the ISO 20022 message
    apphdr_xml, document_xml = generator.generate_iso20022_apphdr_and_pacs008(sample_payload)
    
    # Check that the XML strings are not empty
    assert apphdr_xml
    assert document_xml
    
    # Check that the XML strings contain required elements
    assert '<head:AppHdr' in apphdr_xml
    assert '<pacs:Document' in document_xml
    
    # Check that the XML contains expected data
    assert 'JOHN DOE' in document_xml
    assert 'JANE SMITH' in document_xml


@patch('xmlschema.XMLSchema')
def test_process(mock_xmlschema, sample_payload):
    """Test the full process method with schema validation."""
    # Mock the schemas and validation
    mock_schema = MagicMock()
    mock_xmlschema.return_value = mock_schema
    
    # Mock os.path.exists to return True for schema files
    with patch('os.path.exists', return_value=True):
        # Initialize the generator
        generator = Iso20022CodeGen()
        
        # Process the payload
        result = generator.process(sample_payload)
        
        # Check the result
        assert result["statusCode"] == 200
        assert isinstance(result["body"], str)
        assert '<head:AppHdr' in result["body"]
        assert '<pacs:Document' in result["body"]
        
        # Verify validation was attempted
        assert mock_schema.validate.call_count == 2


def test_process_with_missing_field():
    """Test process method with missing required field."""
    # Create a payload with missing required field
    payload = {
        "fedWireMessage": {
            # Missing inputMessageAccountabilityData
            "amount": {
                "amount": "000000001000"
            }
        }
    }
    
    # Initialize the generator
    generator = Iso20022CodeGen()
    
    # Process the payload
    result = generator.process(payload)
    
    # Check the error response
    assert result["statusCode"] == 400
    assert "error" in json.loads(result["body"])
    assert "Missing required field" in json.loads(result["body"])["error"] 