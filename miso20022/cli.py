# SPDX-License-Identifier: Apache-2.0

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Dict, Any

from miso20022.fedwire import generate_fedwire_message, generate_fedwire_payload
from miso20022.fednow import generate_fednow_message

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

def handle_fedwire_generate(args):
    """Handler for the 'fedwire generate' command."""
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

def handle_fedwire_parse(args):
    """Handler for the 'fedwire parse' command."""
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

def handle_fednow_generate(args):
    """Handler for the 'fednow generate' command."""
    xsd_path = os.path.abspath(args.xsd_file)
    if not os.path.exists(xsd_path):
        print(f"Error: XSD file not found at {xsd_path}", file=sys.stderr)
        sys.exit(1)

    input_path = os.path.abspath(args.input_file)
    if not os.path.exists(input_path):
        print(f"Error: Input file not found at {input_path}", file=sys.stderr)
        sys.exit(1)

    payload = load_input_payload(input_path)
    _, _, complete_message = generate_fednow_message(args.message_code, args.environment, args.fed_aba, payload, xsd_path)

    if complete_message:
        output_file = args.output_file or generate_output_filename(args.message_code, 'xml')
        write_message_to_file(complete_message, output_file)
    else:
        print("Failed to generate complete message", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='A CLI tool for generating and parsing ISO 20022 messages.')
    subparsers = parser.add_subparsers(dest='command', required=True, help='Available commands')

    # Fedwire command
    fedwire_parser = subparsers.add_parser('fedwire', help='FedWire related commands')
    fedwire_subparsers = fedwire_parser.add_subparsers(dest='subcommand', required=True)

    fedwire_gen_parser = fedwire_subparsers.add_parser('generate', help='Generate a complete FedWire ISO 20022 message.')
    fedwire_gen_parser.add_argument('--message_code', help='ISO 20022 message code (e.g., urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08)')
    fedwire_gen_parser.add_argument('--environment', required=True, choices=['TEST', 'PROD'], help='The environment for the message (TEST or PROD).')
    fedwire_gen_parser.add_argument('--fed-aba', required=True, help='The Fed ABA number for message generation.')
    fedwire_gen_parser.add_argument('--input-file', required=True, help='Path to input JSON payload file.')
    fedwire_gen_parser.add_argument('--output-file', help='Path to output XML file.')
    fedwire_gen_parser.add_argument('--xsd-file', required=True, help='Path to the XSD file.')
    fedwire_gen_parser.set_defaults(func=handle_fedwire_generate)

    fedwire_parse_parser = fedwire_subparsers.add_parser('parse', help='Parse a FedWire ISO 20022 XML file into a JSON payload.')
    fedwire_parse_parser.add_argument('--input-file', required=True, help='Path to the XML file to parse.')
    fedwire_parse_parser.add_argument('--message-code', required=True, help='The message code to determine the parsing model.')
    fedwire_parse_parser.add_argument('--output-file', help='Path to output JSON file.')
    fedwire_parse_parser.set_defaults(func=handle_fedwire_parse)

    # Fednow command
    fednow_parser = subparsers.add_parser('fednow', help='FedNow related commands')
    fednow_subparsers = fednow_parser.add_subparsers(dest='subcommand', required=True)

    fednow_gen_parser = fednow_subparsers.add_parser('generate', help='Generate a complete FedNow ISO 20022 message.')
    fednow_gen_parser.add_argument('--message_code', required=True, help='ISO 20022 message code for FedNow.')
    fednow_gen_parser.add_argument('--environment', required=True, choices=['TEST', 'PROD'], help='The environment for the message (TEST or PROD).')
    fednow_gen_parser.add_argument('--fed-aba', required=True, help='The Fed ABA number for message generation.')
    fednow_gen_parser.add_argument('--input-file', required=True, help='Path to input JSON payload file.')
    fednow_gen_parser.add_argument('--output-file', help='Path to output XML file.')
    fednow_gen_parser.add_argument('--xsd-file', required=True, help='Path to the XSD file.')
    fednow_gen_parser.set_defaults(func=handle_fednow_generate)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
