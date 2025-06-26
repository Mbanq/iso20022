import json
import sys
import os
import argparse

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from miso20022.fedwire import generate_fedwire_payload

def main():
    parser = argparse.ArgumentParser(description="Parse ISO20022 XML and convert to Fedwire JSON format.")
    parser.add_argument("xml_file", help="Path to the input XML file.")
    parser.add_argument("message_code", help="The message code (e.g., pacs.008.001.08, pacs.002.001.10).")
    args = parser.parse_args()

    xml_file_path = args.xml_file
    message_code = args.message_code

    if not os.path.exists(xml_file_path):
        print(f"Error: File not found at {xml_file_path}")
        sys.exit(1)

    print(f"Processing file: {xml_file_path} with message code: {message_code}")

    try:
        fedwire_json = generate_fedwire_payload(xml_file_path, message_code)
        
        # Generate output filename
        base_name = os.path.basename(xml_file_path)
        file_name_without_ext = os.path.splitext(base_name)[0]
        output_filename = f'{file_name_without_ext}_output.json'

        with open(output_filename, 'w') as f:
            json.dump(fedwire_json, f, indent=2)
        print(f"Successfully created {output_filename}")

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
