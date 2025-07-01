# Release Notes

## Version 0.1.1

This is the initial public release of `miso20022`, a Python library and command-line tool for generating and parsing ISO 20022 messages, with a focus on US payment rails.

### Key Features

*   **Message Generation**: Create compliant ISO 20022 XML messages from a JSON payload.
*   **CLI and Library**: Use the `miso20022` command-line tool for quick operations or integrate the library into your Python applications.
*   **Environment Support**: Specify the target environment (`TEST` or `PROD`) for message generation, which correctly sets the `BizSvc` field in the Application Header.
*   **Payload Parsing**: Parse existing ISO 20022 XML messages into a structured JSON format.
*   **Comprehensive Documentation**: Includes a `README.md` for project overview and a `PKG_README.md` with detailed library usage and JSON payload structures.
*   **PyPI Distribution**: The package is available for installation from PyPI.

### Supported Message Types

This version provides support for the following Fedwire message types:

#### Generation

*   **`pacs.008.001.08`**: FI to FI Customer Credit Transfer (Full Support)
    *   Generates a complete `pacs.008` message using a dedicated data model.
*   **`pacs.028.001.03`**: FI to FI Payment Status Request (Basic Support)
    *   Generates a structured `pacs.028` message for payment status inquiries.

#### Parsing

*   **`pacs.008.001.08`**: FI to FI Customer Credit Transfer
*   **`pacs.002.001.10`**: FI to FI Payment Status Report

We are actively working to expand the range of supported message types in future releases.
