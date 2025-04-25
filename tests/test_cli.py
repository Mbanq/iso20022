"""
Tests for the command-line interface.
"""
import json
import os
import sys
import tempfile
from unittest.mock import patch, MagicMock

import pytest

from iso20022gen.cli import main


@pytest.fixture
def sample_payload_file():
    """Create a temporary file with sample payment data."""
    payload = {
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
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        json.dump(payload, f)
        file_path = f.name
    
    yield file_path
    
    # Cleanup
    if os.path.exists(file_path):
        os.unlink(file_path)


@patch('iso20022gen.cli.load_json_file')
@patch('iso20022gen.cli.Iso20022CodeGen')
def test_generate_command(mock_generator_class, mock_load_json, sample_payload_file):
    """Test the generate command."""
    # Mock the generator
    mock_generator = MagicMock()
    mock_generator_class.return_value = mock_generator
    
    # Mock the result
    mock_generator.process.return_value = {
        "statusCode": 200,
        "headers": {"Content-Type": "application/xml"},
        "body": "<xml>Test XML</xml>"
    }
    
    # Mock the payload loading with a valid payload
    mock_load_json.return_value = {
        "fedWireMessage": {
            "inputMessageAccountabilityData": {
                "inputCycleDate": "20250109",
                "inputSource": "TEST001",
                "inputSequenceNumber": "000001"
            },
            "amount": {"amount": "000000001000"},
            "senderDepositoryInstitution": {
                "senderABANumber": "121182904",
                "senderShortName": "TEST BANK"
            },
            "receiverDepositoryInstitution": {
                "receiverABANumber": "084106768",
                "receiverShortName": "RECEIVING BANK"
            },
            "beneficiary": {"personal": {"name": "JOHN DOE", "identifier": "123", "address": {}}},
            "originator": {"personal": {"name": "JANE SMITH", "identifier": "456", "address": {}}}
        }
    }
    
    # Capture stdout
    with patch('sys.stdout') as mock_stdout:
        # Run the command
        args = ['generate', sample_payload_file]
        exit_code = main(args)
        
        # Check that the command was successful
        assert exit_code == 0
        
        # Check that the generator was initialized and used
        mock_generator_class.assert_called_once()
        mock_generator.process.assert_called_once()
        
        # Check that output was printed
        mock_stdout.write.assert_called()


@patch('iso20022gen.cli.load_json_file')
@patch('iso20022gen.cli.Iso20022CodeGen')
@patch('iso20022gen.cli.OutgoingFedWire')
def test_generate_command_with_fedwire(mock_fedwire_class, mock_generator_class, mock_load_json, sample_payload_file):
    """Test the generate command with Fedwire wrapping."""
    # Mock the generator
    mock_generator = MagicMock()
    mock_generator_class.return_value = mock_generator
    
    # Mock the Fedwire wrapper
    mock_fedwire = MagicMock()
    mock_fedwire_class.return_value = mock_fedwire
    
    # Mock the results
    mock_generator.process.return_value = {
        "statusCode": 200,
        "headers": {"Content-Type": "application/xml"},
        "body": "<xml>Test XML</xml>"
    }
    mock_fedwire.wrap_in_fedwire_envelope.return_value = "<fedwire>Wrapped XML</fedwire>"
    
    # Mock the payload loading with a valid payload
    mock_load_json.return_value = {
        "fedWireMessage": {
            "inputMessageAccountabilityData": {
                "inputCycleDate": "20250109",
                "inputSource": "TEST001",
                "inputSequenceNumber": "000001"
            },
            "amount": {"amount": "000000001000"},
            "senderDepositoryInstitution": {
                "senderABANumber": "121182904",
                "senderShortName": "TEST BANK"
            },
            "receiverDepositoryInstitution": {
                "receiverABANumber": "084106768",
                "receiverShortName": "RECEIVING BANK"
            },
            "beneficiary": {"personal": {"name": "JOHN DOE", "identifier": "123", "address": {}}},
            "originator": {"personal": {"name": "JANE SMITH", "identifier": "456", "address": {}}}
        }
    }
    
    # Capture stdout
    with patch('sys.stdout') as mock_stdout:
        # Run the command
        args = ['generate', '--fedwire', sample_payload_file]
        exit_code = main(args)
        
        # Check that the command was successful
        assert exit_code == 0
        
        # Check that the generator and wrapper were used
        mock_generator_class.assert_called_once()
        mock_generator.process.assert_called_once()
        mock_fedwire_class.assert_called_once()
        mock_fedwire.wrap_in_fedwire_envelope.assert_called_once_with("<xml>Test XML</xml>")
        
        # Check that output was printed
        mock_stdout.write.assert_called()


@patch('iso20022gen.cli.load_json_file')
@patch('iso20022gen.cli.Iso20022CodeGen')
def test_generate_command_with_output_file(mock_generator_class, mock_load_json, sample_payload_file):
    """Test the generate command with output to file."""
    # Mock the generator
    mock_generator = MagicMock()
    mock_generator_class.return_value = mock_generator
    
    # Mock the result
    mock_generator.process.return_value = {
        "statusCode": 200,
        "headers": {"Content-Type": "application/xml"},
        "body": "<xml>Test XML</xml>"
    }
    
    # Mock the payload loading with a valid payload
    mock_load_json.return_value = {
        "fedWireMessage": {
            "inputMessageAccountabilityData": {
                "inputCycleDate": "20250109",
                "inputSource": "TEST001",
                "inputSequenceNumber": "000001"
            },
            "amount": {"amount": "000000001000"},
            "senderDepositoryInstitution": {
                "senderABANumber": "121182904",
                "senderShortName": "TEST BANK"
            },
            "receiverDepositoryInstitution": {
                "receiverABANumber": "084106768",
                "receiverShortName": "RECEIVING BANK"
            },
            "beneficiary": {"personal": {"name": "JOHN DOE", "identifier": "123", "address": {}}},
            "originator": {"personal": {"name": "JANE SMITH", "identifier": "456", "address": {}}}
        }
    }
    
    # Create a temporary output file
    with tempfile.NamedTemporaryFile(delete=False) as output_file:
        output_path = output_file.name
    
    try:
        # Run the command
        args = ['generate', '--output', output_path, sample_payload_file]
        exit_code = main(args)
        
        # Check that the command was successful
        assert exit_code == 0
        
        # Check that the output file was created and has the expected content
        with open(output_path, 'r') as f:
            content = f.read()
            assert content == "<xml>Test XML</xml>"
    finally:
        # Cleanup
        if os.path.exists(output_path):
            os.unlink(output_path)


def test_version_command():
    """Test the version command."""
    # Capture stdout
    with patch('sys.stdout') as mock_stdout:
        # Run the command
        args = ['version']
        exit_code = main(args)
        
        # Check that the command was successful
        assert exit_code == 0
        
        # Check that output contains version info
        mock_stdout.write.assert_called()


def test_no_command():
    """Test running with no command."""
    # Mock argparse
    with patch('argparse.ArgumentParser.print_help') as mock_print_help:
        # Run without a command
        args = []
        exit_code = main(args)
        
        # Check that help was printed
        assert exit_code == 0
        mock_print_help.assert_called_once() 