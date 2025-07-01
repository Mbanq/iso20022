# ISO20022 Message Generator and Parser

This project provides a comprehensive suite of tools for working with ISO 20022 messages, with a special focus on the US Payment Rails. It includes a message generator, a payload parser, and a web application to streamline the process of creating and handling ISO 20022 messages.

## Key Features

-   **Message Generation**: Create fully compliant ISO 20022 XML messages from a JSON payload.
-   **Payload Parser**: Convert existing ISO 20022 XML messages into a structured JSON payload.
-   **Fedwire Support**: Specialized support for Fedwire messages, including `pacs.008.001.08` and `pacs.028.001.03`.
-   **Web Application**: An intuitive web-based interface for generating messages without writing any code.
-   **Command-Line Tools**: Powerful command-line scripts for both message generation and parsing.
-   **Extensible Library**: A well-structured Python library that can be easily integrated into your own applications.

## Installation

There are two ways to install the project, depending on your needs.

### Standard Installation (Recommended)

If you want to use the `miso20022` library or CLI tools in your own projects, you can install it directly from PyPI:

```bash
pip install miso20022
```

This will download and install the latest stable release.

### Developer Installation

If you want to contribute to the project or need the very latest (unreleased) changes, you should clone the repository and install it in editable mode.

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Mbanq/iso20022.git
    cd iso20022
    ```

2.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Install the package in editable mode:**

    This allows you to make changes to the source code and have them immediately reflected in your environment.

    ```bash
    pip install -e .
    ```

## Usage

This project offers three primary ways to interact with ISO 20022 messages: the command-line interface, the web application, and the Python library.

### 1. Command-Line Interface (CLI)

The CLI provides a single entry point, `miso20022`, with two main commands: `generate` for creating messages and `parse` for parsing them.

#### Message Generation (`generate`)

This command generates a complete ISO 20022 message from a JSON payload.

**Usage:**

```bash
miso20022 generate --message_code [MESSAGE_CODE] --environment [ENV] --fed-aba [ABA_NUMBER] --input-file [PAYLOAD_FILE] --output-file [OUTPUT_XML]
```

**Arguments:**

-   `--message_code`: The ISO 20022 message code (e.g., `urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08`).
-   `--environment`: The environment for the message (`TEST` or `PROD`).
-   `--fed-aba`: The Fedwire ABA number.
-   `--input-file`: Path to the input JSON payload file.
-   `--output-file`: (Optional) Path to save the generated XML message. If not provided, a filename will be generated automatically.
-   `--xsd-file`: Path to the XSD file for validation. Defaults to `proprietary_Fed_Format.xsd`.

**Example:**

```bash
miso20022 generate \
    --message_code urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08 \
    --environment TEST \
    --fed-aba 00088444 \
    --input-file sample_files/sample_payment.json \
    --output-file pacs.008_output.xml
```

#### Payload Parser (`parse`)

This command parses an existing ISO 20022 XML file and converts it into a JSON payload.

**Usage:**

```bash
miso20022 parse --input-file [INPUT_XML] --message-code [MESSAGE_CODE] --output-file [OUTPUT_JSON]
```

**Arguments:**

-   `--input-file`: Path to the input ISO 20022 XML file.
-   `--message-code`: The ISO 20022 message code of the input file.
-   `--output-file`: (Optional) Path to save the output JSON payload. If not provided, a filename will be generated automatically.

**Example:**

```bash
miso20022 parse \
    --input-file sample_files/pacs.008.001.008_2025_1.xml \
    --message-code urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08 \
    --output-file parsed_payload.json
```

This will create a `parsed_payload.json` file in the current directory.

### 2. Web Application

The web application provides a user-friendly interface for generating ISO 20022 messages.

**Running the Web App:**

1.  **Install web dependencies (if not already installed):**

    ```bash
    pip install Flask Werkzeug
    ```

2.  **Run the application:**

    ```bash
    python3 webapp/app.py
    ```

3.  **Access the application:**

    Open your web browser and navigate to `http://127.0.0.1:5000`.

**Features:**

-   Upload an XSD file for schema validation.
-   Provide a JSON payload by uploading a file or pasting text.
-   Specify the message code.
-   Generate and download the resulting ISO 20022 XML message.

### 3. Python Library (`miso20022`)

The core logic of this project is also available as a standalone Python package, `miso20022`. This is ideal if you want to integrate ISO 20022 message generation directly into your own applications.

For detailed instructions on how to use the library, including installation and code examples, please see the [package-specific README](./miso20022/README.md).


## Supported Message Types

The library has built-in support for the following Fedwire message types:

-   `pacs.008.001.08`: FI to FI Customer Credit Transfer
-   `pacs.028.001.03`: FI to FI Payment Status Request

Support for other message types can be added by extending the data models in the `miso20022` module.

## Project Structure

```
.

├── LICENSE
├── README.md
├── miso20022/
│   ├── README.md
│   ├── __init__.py
│   ├── bah/ # Contains the bah message models
│   ├── cli.py # Contains the command line interface
│   ├── fedwire.py # Contains the fedwire message generator
│   ├── helpers.py # Contains the helper functions
│   └── pacs/ # Contains the pacs message models
├── pyproject.toml # Contains the project metadata
├── webapp # Contains the web application
├── validate_xml.py # Contains the xml validator
└── venv/ # Contains the virtual environment
```

## Fedwire Payments

This project can be used to generate the message content for Fedwire payments, which utilize the ISO 20022 standard. However, the message envelope format for Fedwire is proprietary. Users must obtain the necessary proprietary XSD files from the Federal Reserve and integrate them to create complete Fedwire messages. This project does not include any proprietary information or files.

For more information on Fedwire's ISO 20022 implementation and to access the required files, please visit the [Federal Reserve ISO 20022 Implementation Center](https://www.frbservices.org/resources/financial-services/wires/iso-20022-implementation-center).


### Important Notice on Proprietary Envelope
The Fedwire envelope format is proprietary and must be implemented according to the Federal Reserve specifications. This library only generates the ISO 20022 message content and wraps them in the message envelope only if the propietory XSD is provided.

For Fedwire: 

[Get Access to Prorietory XSD](https://www.frbservices.org/binaries/content/assets/crsocms/resources/financial-services/request-access-fedwire-funds-iso-20022-technical-guide.pdf)

For official information about Fedwire ISO 20022 implementation, including envelope specifications, please consult the following resources:

- [Federal Reserve ISO 20022 Implementation Center](https://www.frbservices.org/resources/financial-services/wires/iso-20022-implementation-center)
- [Federal Reserve's MyStandards platform](https://www2.swift.com/mystandards/#/group/Federal_Reserve_Financial_Services/Fedwire_Funds_Service)
- [The Fedwire Funds Service ISO 20022 Implementation Guide and Technical Guide](https://www.frbservices.org/resources/financial-services/wires/iso-20022-implementation-center)

## Contributing

Contributions are welcome! Please feel free to open an issue for any bugs, feature requests, or improvements.

## Issues and Bug Reports

If you encounter any bugs or have a feature request, please open an issue on our [GitHub Issues page](https://github.com/Mbanq/iso20022/issues).

When reporting a bug, please include the following information:

-   A clear and concise description of the issue.
-   Steps to reproduce the behavior.
-   The expected behavior.
-   The actual behavior.
-   Your operating system and Python version.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

