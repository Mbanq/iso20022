# SPDX-License-Identifier: Apache-2.0

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Dict, Any

from miso20022.fedwire import generate_fedwire_message, generate_fedwire_payload

def load_input_payload(input_file_path: str) -> Dict[str, Any]:
    """Load a input payload from a JSON file."""
    try:
        with open(input_file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading input file: {e}", file=sys.stderr)
        sys.exit(1)

def write_message_to_file(message: str, output_file: str) -> bool:
    """Write the generated message to a file."""
    try:
        with open(output_file, 'w') as file:
            file.write(message)
        print(f"Message successfully written to {output_file}")
        return True
    except Exception as e:
        print(f"Error writing message to file: {e}", file=sys.stderr)
        return False

def generate_output_filename(message_code: str, extension: str) -> str:
    """Generate a default output filename."""
    message_type = message_code.split(':')[-1]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{message_type}_{timestamp}.{extension}"

def handle_generate(args):
    """Handler for the 'generate' command."""
    xsd_path = os.path.abspath(args.xsd_file)
    if not os.path.exists(xsd_path):
        print(f"Error: XSD file not found at {xsd_path}", file=sys.stderr)
        sys.exit(1)

    input_path = os.path.abspath(args.input_file)
    if not os.path.exists(input_path):
        print(f"Error: Input file not found at {input_path}", file=sys.stderr)
        sys.exit(1)

    payload = load_input_payload(input_path)
    _, _, complete_message = generate_fedwire_message(args.message_code, args.environment, args.fed_aba, payload, xsd_path)

    if complete_message:
        output_file = args.output_file or generate_output_filename(args.message_code, 'xml')
        write_message_to_file(complete_message, output_file)
    else:
        print("Failed to generate complete message", file=sys.stderr)
        sys.exit(1)

def handle_parse(args):
    """Handler for the 'parse' command."""
    if not os.path.exists(args.input_file):
        print(f"Error: Input file not found at {args.input_file}", file=sys.stderr)
        sys.exit(1)

    payload = generate_fedwire_payload(args.input_file, args.message_code)

    if payload:
        output_file = args.output_file or generate_output_filename(args.message_code, 'json')
        try:
            with open(output_file, 'w') as f:
                json.dump(payload, f, indent=4)
            print(f"Payload successfully written to {output_file}")
        except Exception as e:
            print(f"Error writing payload to file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("Failed to parse XML file.", file=sys.stderr)
        sys.exit(1)

def main():

    parser = argparse.ArgumentParser(description='A CLI tool for generating and parsing ISO 20022 messages.')
    subparsers = parser.add_subparsers(dest='command', required=True, help='Available commands')

    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate a complete ISO 20022 message.')
    gen_parser.add_argument('--message_code', help='ISO 20022 message code (e.g., urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08)')
    gen_parser.add_argument('--environment', required=True, choices=['TEST', 'PROD'], help='The environment for the message (TEST or PROD).')
    gen_parser.add_argument('--fed-aba', required=True, help='The Fed ABA number for message generation.')
    gen_parser.add_argument('--input-file', required=True, help='Path to input JSON payload file.')
    gen_parser.add_argument('--output-file', help='Path to output XML file.')
    gen_parser.add_argument('--xsd-file', required=True, help='Path to the XSD file.')
    gen_parser.set_defaults(func=handle_generate)

    # Parse command
    parse_parser = subparsers.add_parser('parse', help='Parse an ISO 20022 XML file into a JSON payload.')
    parse_parser.add_argument('--input-file', required=True, help='Path to the XML file to parse.')
    parse_parser.add_argument('--message-code', required=True, help='The message code to determine the parsing model.')
    parse_parser.add_argument('--output-file', help='Path to output JSON file.')
    parse_parser.set_defaults(func=handle_parse)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
