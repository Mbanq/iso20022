"""
Command-line interface for ISO20022Gen.
"""
import argparse
import json
import logging
import os
import sys
from typing import Dict, Any, List, Optional

from iso20022gen import Iso20022CodeGen, configure

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def setup_parser() -> argparse.ArgumentParser:
    """Set up the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="ISO20022Gen - Generate ISO 20022 compliant financial messages",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Global options
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--config", "-c",
        help="Path to configuration file"
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Generate command
    generate_parser = subparsers.add_parser(
        "generate",
        help="Generate ISO 20022 message from JSON payload"
    )
    generate_parser.add_argument(
        "input_file",
        help="JSON input file with payment data"
    )
    generate_parser.add_argument(
        "--output", "-o",
        help="Output file for generated XML (default: stdout)"
    )
    generate_parser.add_argument(
        "--schemas", "-s",
        help="Path to XSD schema files"
    )
    
    # Note on Fedwire envelope handling
    generate_parser.epilog = (
        "NOTE: This library only generates ISO 20022 message content (AppHdr and Document). "
        "The proprietary Fedwire envelope is not generated. For information on Fedwire envelope "
        "specifications, visit: "
        "https://www.frbservices.org/resources/financial-services/wires/iso-20022-implementation-center"
    )
    
    # Version command
    version_parser = subparsers.add_parser(
        "version",
        help="Show version information"
    )
    
    return parser


def load_json_file(file_path: str) -> Dict[str, Any]:
    """
    Load JSON from file.
    
    Args:
        file_path: Path to the JSON file.
        
    Returns:
        Parsed JSON data.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in file: {file_path}")
        raise


def generate_message(args: argparse.Namespace) -> int:
    """
    Generate ISO 20022 message from JSON payload.
    
    Args:
        args: Command-line arguments.
        
    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    # Load input payload
    try:
        payload = load_json_file(args.input_file)
    except (FileNotFoundError, json.JSONDecodeError):
        return 1
        
    # Initialize generator
    generator = Iso20022CodeGen(schemas_path=args.schemas)
    
    # Process payload
    result = generator.process(payload)
    
    if result["statusCode"] != 200:
        logger.error(f"Error generating message: {result['body']}")
        return 1
        
    # Get the generated message
    message = result["body"]
    
    # Output the message
    if args.output:
        try:
            with open(args.output, "w") as f:
                f.write(message)
            logger.info(f"Message written to: {args.output}")
        except Exception as e:
            logger.error(f"Error writing to output file: {e}")
            return 1
    else:
        print(message)
        
    return 0


def show_version() -> int:
    """
    Show version information.
    
    Returns:
        Exit code (always 0).
    """
    from iso20022gen import __version__
    print(f"ISO20022Gen version {__version__}")
    return 0


def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the command-line interface.
    
    Args:
        args: Command-line arguments (defaults to sys.argv if None).
        
    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    parser = setup_parser()
    parsed_args = parser.parse_args(args)
    
    # Configure logging level
    if parsed_args.verbose:
        logging.getLogger("iso20022gen").setLevel(logging.DEBUG)
    
    # Load configuration if specified
    if parsed_args.config:
        try:
            config_data = load_json_file(parsed_args.config)
            configure(config_dict=config_data)
        except (FileNotFoundError, json.JSONDecodeError):
            return 1
    
    # Execute command
    if parsed_args.command == "generate":
        return generate_message(parsed_args)
    elif parsed_args.command == "version":
        return show_version()
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main()) 