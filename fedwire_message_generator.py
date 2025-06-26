#!/usr/bin/env python3
"""
Fedwire Message Generator

This script generates ISO20022-compliant Fedwire messages by parsing an XSD file,
identifying the structure of a specific message code, and generating
complete Fedwire messages using models and sample data.
"""

import os
import sys
import json
import argparse
from typing import Optional, Dict, Any
from datetime import datetime

# Import the fedwire module functions
from miso20022.fedwire import generate_fedwire_message, generate_message_structure


def load_sample_payload(sample_file_path: str) -> Dict[str, Any]:
    """
    Load a sample payload from a JSON file.
    
    Args:
        sample_file_path: Path to the sample JSON file
        
    Returns:
        The loaded JSON data
    """
    try:
        with open(sample_file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading sample file: {e}")
        sys.exit(1)

def write_message_to_file(message: str, output_file: str) -> bool:
    """
    Write the generated message to a file.
    
    Args:
        message: The XML message to write
        output_file: Path to the output file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(output_file, 'w') as file:
            file.write(message)
        print(f"Message successfully written to {output_file}")
        return True
    except Exception as e:
        print(f"Error writing message to file: {e}")
        return False

def generate_output_filename(message_code: str) -> str:
    """
    Generate a default output filename based on the message code and current timestamp.
    
    Args:
        message_code: The ISO20022 message code
        
    Returns:
        A filename string
    """
    import datetime
    
    # Extract the message type from the message code
    message_type = message_code.split(':')[-1]
    
    # Generate timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    return f"{message_type}_{timestamp}.xml"

def main():
    """Main function to process command line arguments and execute the appropriate action."""
    parser = argparse.ArgumentParser(description='ISO20022 Message Structure Identifier')
    parser.add_argument('message_code', nargs='?', help='ISO20022 message code (e.g., urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08)')
    parser.add_argument('--generate', action='store_true', help='Generate a complete message using models')
    parser.add_argument('--fed-aba', help='The Fed ABA number for message generation')
    parser.add_argument('--sample-file', help='Path to sample JSON payload file for message generation')
    parser.add_argument('--output-file', help='Path to output XML file for the generated message')
    parser.add_argument('--xsd-file', default='proprietary_xsd/fedwirefunds-incoming.xsd', help='Path to the XSD file')
    
    args = parser.parse_args()
    
    # Get the absolute path to the XSD file
    xsd_path = os.path.abspath(args.xsd_file)
    
    # Check if the XSD file exists
    if not os.path.exists(xsd_path):
        print(f"Error: XSD file not found at {xsd_path}")
        sys.exit(1)
    
    # Generate a complete message
    if args.generate:
        if not args.message_code:
            print("Error: Message code is required for generation")
            sys.exit(1)
        
        # Set default sample file if not provided
        if args.sample_file:
            sample_path = os.path.abspath(args.sample_file)
        else:
            # Use the default sample file in the sample_files directory
            sample_path = os.path.abspath(os.path.join(
                os.path.dirname(__file__),
                'sample_files',
                'sample_payload.json'
            ))
        
        if not os.path.exists(sample_path):
            print(f"Error: Sample file not found at {sample_path}")
            sys.exit(1)
        
        # Load the sample payload
        payload = load_sample_payload(sample_path)
        
        # Generate the complete message
        _, _, complete_message = generate_fedwire_message(args.message_code, args.fed_aba, payload, xsd_path)
        
        if complete_message:
            print("Complete Message Structure:")
            print(complete_message)
            
            # Write to file if requested or use default filename
            output_file = args.output_file
            if not output_file:
                output_file = generate_output_filename(args.message_code)
            
            write_message_to_file(complete_message, output_file)
        else:
            print("Failed to generate complete message")
            sys.exit(1)
        
        return
    
    # If no specific action is specified, just show the message structure
    if args.message_code:
        try:
            # Use the appropriate sample payload based on message type
            sample_file_path = ''
            if "pacs.008" in args.message_code:
                sample_file_path = os.path.join(
                    os.path.dirname(__file__),
                    'sample_files',
                    'sample_payload.json'
                )
            elif "pacs.028" in args.message_code:
                sample_file_path = os.path.join(
                    os.path.dirname(__file__),
                    'sample_files',
                    'sample_pacs028_payload.json'
                )
            else:
                # Default to the standard sample payload
                sample_file_path = os.path.join(
                    os.path.dirname(__file__),
                    'sample_files',
                    'sample_payload.json'
                )
            
            # Check if the sample file exists
            if not os.path.exists(sample_file_path):
                print(f"Error: Sample file not found at {sample_file_path}")
                sys.exit(1)
                
            # Load the sample payload
            sample_payload = load_sample_payload(sample_file_path)
            
            # Generate the message structure
            app_hdr_xml, document_xml, structure = generate_fedwire_message(args.message_code, args.fed_aba, sample_payload, xsd_path)
            if structure:
                print("Message Structure:")
                print(structure)
            else:
                sys.exit(1)
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
