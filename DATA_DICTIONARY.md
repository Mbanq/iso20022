# JSON Payload Data Dictionary

This document describes the structure and fields of the JSON payloads used in this project, based on the `sample_*.json` files.

## Common Structure

The following fields are common across different message types.

### `fedWireMessage` (Object)

The main container for the FedWire message data.

| Field | Type | Description |
| :--- | :--- | :--- |
| `inputMessageAccountabilityData` | Object | Contains metadata about the message. |
| `amount` | Object | **Optional**. Contains the transaction amount. Present in `pacs.008` messages. |
| `senderDepositoryInstitution` | Object | Information about the sender's financial institution. |
| `receiverDepositoryInstitution` | Object | Information about the receiver's financial institution. |
| `originator` | Object | **Optional**. Information about the originator of the funds. Present in `pacs.008` messages. |
| `beneficiary` | Object | **Optional**. Information about the beneficiary of the funds. Present in `pacs.008` messages. |

### `receiverRoutingNumber` (String)

The routing number of the receiving institution.

---

## Detailed Field Descriptions

### `inputMessageAccountabilityData`

| Field | Type | Description |
| :--- | :--- | :--- |
| `inputCycleDate` | String | The date of the message cycle in `YYYYMMDD` format. |
| `inputSource` | String | The source of the message (e.g., `MBANQ`). |
| `inputSequenceNumber` | String | The sequence number of the message. |

### `amount`

| Field | Type | Description |
| :--- | :--- | :--- |
| `amount` | String | The transaction amount, represented as a string of digits (e.g., `1001134` for $10,011.34). |

### `senderDepositoryInstitution`

| Field | Type | Description |
| :--- | :--- | :--- |
| `senderABANumber` | String | The ABA routing number of the sender's institution. |
| `senderShortName` | String | The short name of the sender's institution. |

### `receiverDepositoryInstitution`

| Field | Type | Description |
| :--- | :--- | :--- |
| `receiverABANumber` | String | The ABA routing number of the receiver's institution. |
| `receiverShortName` | String | The short name of the receiver's institution. |

### `originator` / `beneficiary`

These objects share the same structure.

| Field | Type | Description |
| :--- | :--- | :--- |
| `personal` | Object | Personal details of the individual. |

#### `personal` Object

| Field | Type | Description |
| :--- | :--- | :--- |
| `name` | String | The full name of the individual. |
| `address` | Object | The postal address of the individual. |
| `identifier` | String | A unique identifier for the individual. |

##### `address` Object

| Field | Type | Description |
| :--- | :--- | :--- |
| `addressLineOne` | String | The first line of the address. |
| `addressLineTwo` | String | The second line of the address. |
| `addressLineThree` | String | **Optional**. The third line of the address. |

---

## `pacs.028` Specific Fields

The following fields are specific to the `pacs.028` (Payment Status Request) message payload.

| Field | Type | Description |
| :--- | :--- | :--- |
| `message_id` | String | A unique identifier for the `pacs.028` message itself. |
| `original_msg_id` | String | The message ID of the original message being referenced (e.g., a `pacs.008` message). |
| `original_msg_nm_id` | String | The message name identifier of the original message (e.g., `pacs.008.001.08`). |
| `original_creation_datetime` | String | The creation timestamp of the original message in ISO 8601 format. |
| `original_end_to_end_id` | String | The end-to-end identifier from the original message. |
