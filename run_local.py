# SPDX-License-Identifier: Apache-2.0

import sys
import os

# Add the project root to the Python path to ensure local modules are found.
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from miso20022.cli import main

if __name__ == '__main__':
    # This script allows running the CLI with local code changes without installation.
    # Example usage:
    # python run_local.py generate --message_code <message_code> ...
    # python run_local.py parse --input-file <file_path> ...
    main()
