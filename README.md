# ISO20022 Message Generator and Parser

This project provides a comprehensive suite of tools for working with ISO 20022 messages, with a special focus on the Fedwire Funds Service. It includes a message generator, a payload parser, and a web application to streamline the process of creating and handling ISO 20022 messages.

## Key Features

-   **Message Generation**: Create fully compliant ISO 20022 XML messages from a JSON payload.
-   **Payload Parser**: Convert existing ISO 20022 XML messages into a structured JSON payload.
-   **Fedwire Support**: Specialized support for Fedwire messages, including `pacs.008.001.08` and `pacs.028.001.03`.
-   **Web Application**: An intuitive web-based interface for generating messages without writing any code.
-   **Command-Line Tools**: Powerful command-line scripts for both message generation and parsing.
-   **Extensible Library**: A well-structured Python library that can be easily integrated into your own applications.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/iso20022.git
    cd iso20022
    ```

2.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Install the package in editable mode:**

    ```bash
    pip install -e .
    ```

## Usage

This project offers three primary ways to interact with ISO 20022 messages: the command-line interface, the web application, and the Python library.

### 1. Command-Line Interface (CLI)

The CLI provides two main scripts: `fedwire_message_generator.py` for creating messages and `fedwire_payload_parser.py` for parsing them.

#### Message Generation (`fedwire_message_generator.py`)

This script generates a complete ISO 20022 message from a JSON payload.

**Usage:**

```bash
python3 fedwire_message_generator.py --generate --sample-file [PAYLOAD_FILE] --output-file [OUTPUT_XML] --fed-aba [ABA_NUMBER] [MESSAGE_CODE]
```

**Arguments:**

-   `--generate`: Flag to indicate that a message should be generated.
-   `--sample-file`: Path to the input JSON payload file.
-   `--output-file`: Path to save the generated XML message.
-   `--fed-aba`: The Fedwire ABA number.
-   `MESSAGE_CODE`: The ISO 20022 message code (e.g., `urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08`).

**Example:**

```bash
python3 fedwire_message_generator.py \
    --generate \
    --sample-file sample_files/sample_payload.json \
    --output-file pacs.008_output.xml \
    --fed-aba 021151080 \
    urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08
```

#### Payload Parser (`fedwire_payload_parser.py`)

This script parses an existing ISO 20022 XML file and converts it into a JSON payload.

**Usage:**

```bash
python3 fedwire_payload_parser.py [INPUT_XML] [MESSAGE_CODE]
```

**Arguments:**

-   `INPUT_XML`: Path to the input ISO 20022 XML file.
-   `MESSAGE_CODE`: The ISO 20022 message code of the input file.

**Example:**

```bash
python3 fedwire_payload_parser.py sample_files/pacs.008.001.008_2025_1.xml pacs.008.001.08
```

This will create a `pacs.008.001.008_2025_1_output.json` file in the same directory.

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

### 3. Python Library (`mb-iso20022`)

The core logic of this project is also available as a standalone Python package, `mb-iso20022`. This is ideal if you want to integrate ISO 20022 message generation directly into your own applications.

For detailed instructions on how to use the library, including installation and code examples, please see the [package-specific README](./mb_iso20022/README.md).


## Supported Message Types

The library has built-in support for the following Fedwire message types:

-   `pacs.008.001.08`: FI to FI Customer Credit Transfer
-   `pacs.028.001.03`: FI to FI Payment Status Request

Support for other message types can be added by extending the data models in the `mb_iso20022` module.

## Project Structure

```
.
├── fedwire_message_generator.py  # CLI for generating messages
├── fedwire_payload_parser.py     # CLI for parsing messages
├── mb_iso20022/                  # Core Python library
│   ├── __init__.py
│   ├── bah/                      # Business Application Header models
│   ├── common/                   # Common data models
│   ├── pacs/                     # Payments Clearing and Settlement models
│   └── ...
├── schemas/                      # XSD schema files
├── sample_files/                 # Sample XML and JSON files
├── webapp/                       # Flask web application
│   ├── app.py
│   └── templates/
│       └── index.html
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs, feature requests, or improvements.
