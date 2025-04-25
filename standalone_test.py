#!/usr/bin/env python3
"""
Standalone test of model-based XML generation.
"""
import json
import sys
from datetime import datetime
from typing import Dict, Any, List, Optional
from uuid import uuid4

import xmltodict


class AppHdr:
    """Simple AppHdr model."""
    
    @classmethod
    def from_payload(cls, payload):
        """Create AppHdr XML from payload."""
        fedwire_message = payload["fedWireMessage"]
        input_msg_data = fedwire_message["inputMessageAccountabilityData"]
        message_id = f"{input_msg_data['inputCycleDate']}{input_msg_data['inputSource']}{input_msg_data['inputSequenceNumber']}"
        
        sender_aba = fedwire_message["senderDepositoryInstitution"]["senderABANumber"]
        receiver_aba = payload.get("receiverRoutingNumber", "021151080")
        
        return {
            "head:AppHdr": {
                "@xmlns:head": "urn:iso:std:iso:20022:tech:xsd:head.001.001.03",
                "head:Fr": {
                    "head:FIId": {
                        "head:FinInstnId": {
                            "head:ClrSysMmbId": {
                                "head:MmbId": sender_aba
                            }
                        }
                    }
                },
                "head:To": {
                    "head:FIId": {
                        "head:FinInstnId": {
                            "head:ClrSysMmbId": {
                                "head:MmbId": receiver_aba
                            }
                        }
                    }
                },
                "head:BizMsgIdr": message_id,
                "head:MsgDefIdr": "pacs.008.001.08",
                "head:BizSvc": "TEST",
                "head:MktPrctc": {
                    "head:Regy": "www2.swift.com/mystandards/#/group/Federal_Reserve_Financial_Services/Fedwire_Funds_Service",
                    "head:Id": "frb.fedwire.01"
                },
                "head:CreDt": datetime.now().isoformat()
            }
        }


class Document:
    """Simple Document model."""
    
    @staticmethod
    def _add_address_lines(address: Dict[str, str]) -> List[str]:
        """Extract address lines from the address dictionary."""
        address_lines = []
        for key in ["addressLineOne", "addressLineTwo", "addressLineThree"]:
            line = address.get(key, "").replace("NA", "")
            if line:
                address_lines.append(line[:35])
        return address_lines
    
    @classmethod
    def from_payload(cls, payload):
        """Create Document XML from payload."""
        fedwire_message = payload["fedWireMessage"]
        input_msg_data = fedwire_message["inputMessageAccountabilityData"]
        message_id = f"{input_msg_data['inputCycleDate']}{input_msg_data['inputSource']}{input_msg_data['inputSequenceNumber']}"
        
        # Convert amount from cents to dollars
        amount_val = float(fedwire_message["amount"]["amount"]) / 100
        amount_str = str(amount_val)
        
        # Format settlement date
        intrbk_sttlm_dt = datetime.strptime(input_msg_data["inputCycleDate"], "%Y%m%d").strftime("%Y-%m-%d")
        
        # Originator and Beneficiary info
        originator = fedwire_message["originator"]["personal"]
        beneficiary = fedwire_message["beneficiary"]["personal"]
        
        # Create AdrLine list for originator and beneficiary
        originator_addr_lines = cls._add_address_lines(originator["address"])
        beneficiary_addr_lines = cls._add_address_lines(beneficiary["address"])
        
        return {
            "pacs:Document": {
                "@xmlns:pacs": "urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08",
                "pacs:FIToFICstmrCdtTrf": {
                    "pacs:GrpHdr": {
                        "pacs:MsgId": message_id,
                        "pacs:CreDtTm": datetime.now().isoformat(),
                        "pacs:NbOfTxs": "1",
                        "pacs:SttlmInf": {
                            "pacs:SttlmMtd": "CLRG",
                            "pacs:ClrSys": {
                                "pacs:Cd": "FDW"
                            }
                        }
                    },
                    "pacs:CdtTrfTxInf": {
                        "pacs:PmtId": {
                            "pacs:EndToEndId": f"MEtoEID{uuid4().hex[:8]}",
                            "pacs:UETR": str(uuid4())
                        },
                        "pacs:PmtTpInf": {
                            "pacs:LclInstrm": {
                                "pacs:Prtry": "CTRC"
                            }
                        },
                        "pacs:IntrBkSttlmAmt": {
                            "@Ccy": "USD",
                            "#text": amount_str
                        },
                        "pacs:IntrBkSttlmDt": intrbk_sttlm_dt,
                        "pacs:InstdAmt": {
                            "@Ccy": "USD",
                            "#text": amount_str
                        },
                        "pacs:ChrgBr": "SLEV",
                        "pacs:InstgAgt": {
                            "pacs:FinInstnId": {
                                "pacs:ClrSysMmbId": {
                                    "pacs:ClrSysId": {
                                        "pacs:Cd": "USABA"
                                    },
                                    "pacs:MmbId": fedwire_message["senderDepositoryInstitution"]["senderABANumber"]
                                }
                            }
                        },
                        "pacs:InstdAgt": {
                            "pacs:FinInstnId": {
                                "pacs:ClrSysMmbId": {
                                    "pacs:ClrSysId": {
                                        "pacs:Cd": "USABA"
                                    },
                                    "pacs:MmbId": fedwire_message["receiverDepositoryInstitution"]["receiverABANumber"]
                                }
                            }
                        },
                        "pacs:Dbtr": {
                            "pacs:Nm": originator["name"],
                            "pacs:PstlAdr": {
                                "pacs:AdrLine": originator_addr_lines
                            }
                        },
                        "pacs:DbtrAcct": {
                            "pacs:Id": {
                                "pacs:Othr": {
                                    "pacs:Id": originator["identifier"]
                                }
                            }
                        },
                        "pacs:DbtrAgt": {
                            "pacs:FinInstnId": {
                                "pacs:ClrSysMmbId": {
                                    "pacs:ClrSysId": {
                                        "pacs:Cd": "USABA"
                                    },
                                    "pacs:MmbId": fedwire_message["senderDepositoryInstitution"]["senderABANumber"]
                                },
                                "pacs:Nm": fedwire_message["senderDepositoryInstitution"]["senderShortName"],
                                "pacs:PstlAdr": {
                                    "pacs:AdrLine": ["45, 123 Main Street, New York, NY", "10001, US"]
                                }
                            }
                        },
                        "pacs:CdtrAgt": {
                            "pacs:FinInstnId": {
                                "pacs:ClrSysMmbId": {
                                    "pacs:ClrSysId": {
                                        "pacs:Cd": "USABA"
                                    },
                                    "pacs:MmbId": fedwire_message["receiverDepositoryInstitution"]["receiverABANumber"]
                                },
                                "pacs:Nm": fedwire_message["receiverDepositoryInstitution"]["receiverShortName"],
                                "pacs:PstlAdr": {
                                    "pacs:AdrLine": ["45, 123 Main Street, New York, NY", "10001, US"]
                                }
                            }
                        },
                        "pacs:Cdtr": {
                            "pacs:Nm": beneficiary["name"],
                            "pacs:PstlAdr": {
                                "pacs:AdrLine": beneficiary_addr_lines
                            }
                        },
                        "pacs:CdtrAcct": {
                            "pacs:Id": {
                                "pacs:Othr": {
                                    "pacs:Id": beneficiary["identifier"]
                                }
                            }
                        }
                    }
                }
            }
        }


def dict_to_xml(data):
    """Convert dictionary to XML."""
    return xmltodict.unparse(data, pretty=True, full_document=True)


def test_standalone(payload_file):
    """Test the model-based XML generation."""
    # Load the payload from file
    with open(payload_file, "r") as f:
        payload = json.load(f)
    
    # Create models
    app_hdr_dict = AppHdr.from_payload(payload)
    document_dict = Document.from_payload(payload)
    
    # Convert to XML
    app_hdr_xml = dict_to_xml(app_hdr_dict)
    document_xml = dict_to_xml(document_dict)
    
    # Print the XML
    print("AppHdr XML:")
    print(app_hdr_xml)
    print("\nDocument XML:")
    print(document_xml)
    
    # Combined XML - need to remove XML declarations from one of them
    document_xml_without_decl = document_xml.split('?>', 1)[1].strip()
    combined_xml = app_hdr_xml + "\n" + document_xml_without_decl
    
    # Save to file
    with open("output.xml", "w") as f:
        f.write(combined_xml)
    
    print("\nCombined XML saved to output.xml")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python standalone_test.py <payload.json>")
        sys.exit(1)
    
    payload_file = sys.argv[1]
    test_standalone(payload_file) 