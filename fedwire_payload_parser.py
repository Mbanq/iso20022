import json
import sys
import os
import glob

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from iso20022gen.models.fedwire import generate_fedwire_payload


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sample_files_pattern = os.path.join(script_dir, 'sample_files', 'pacs.008.001.008_*.xml')

    xml_files = glob.glob(sample_files_pattern)

    if not xml_files:
        print(f"Error: No pacs.008.001.08 XML files found matching pattern {sample_files_pattern}.")
        sys.exit(1)
    
    latest_xml_file_path = max(xml_files, key=os.path.getctime)
    
    print(f"Processing file: {latest_xml_file_path}")

    try:
        fedwire_json = generate_fedwire_payload(latest_xml_file_path)
        output_filename = 'fedwire_payment_output.json' # This will be in CWD
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
