#!/usr/bin/env python3
"""
Generate a sample PACS.028 payment status request message.
"""

import json
import os
from datetime import datetime, timezone

from iso20022gen.models.head.apphdr import (
    AppHdr, Fr, To, FIId, FinInstnId, ClrSysMmbId, MktPrctc
)
from iso20022gen.models.pacs.pacs028 import Document
from iso20022gen.models.xml_converter import dict_to_xml


def main():
    # Create a PACS.028 payment status request
    document = Document.from_payload(
        msg_id="20250310Scenario03Step2MsgId001",
        original_msg_id="20250310B1QDRCQR000001",
        original_msg_nm_id="pacs.008.001.08",
        original_creation_datetime="2025-03-10T09:00:00-04:00",
        original_instr_id="Scenario01InstrId001",
        original_end_to_end_id="Scenario01EtoEId001",
        original_uetr="8a562c67-ca16-48ba-b074-65581be6f011",
        instg_agt_id="011104238",
        instd_agt_id="021151080"
    )
    
    # Create an application header
    app_hdr = AppHdr(
        Fr=Fr(
            FIId=FIId(
                FinInstnId=FinInstnId(
                    ClrSysMmbId=ClrSysMmbId(MmbId="011104238")
                )
            )
        ),
        To=To(
            FIId=FIId(
                FinInstnId=FinInstnId(
                    ClrSysMmbId=ClrSysMmbId(MmbId="021151080")
                )
            )
        ),
        BizMsgIdr="20250310Scenario03Step2MsgId001",
        MsgDefIdr="pacs.028.001.03",
        BizSvc="TEST",
        MktPrctc=MktPrctc(
            Regy="www2.swift.com/mystandards/#/group/Federal_Reserve_Financial_Services/Fedwire_Funds_Service",
            Id="frb.fedwire.01"
        ),
        CreDt=datetime.now(timezone.utc).isoformat()
    )
    
    # Generate XML
    app_hdr_xml = dict_to_xml(app_hdr.to_dict(), prefix="head", namespace="urn:iso:std:iso:20022:tech:xsd:head.001.001.03")
    document_xml = dict_to_xml(document.to_dict(), prefix="pacs", namespace="urn:iso:std:iso:20022:tech:xsd:pacs.028.001.03")
    
    # Print the XML
    print("Generated XML files:\n")
    print("AppHdr XML:")
    print(app_hdr_xml)
    print("\nDocument XML:")
    print(document_xml)
    
    # Combine the XML files
    combined_xml = f"{app_hdr_xml}\n{document_xml}"
    
    # Save the combined XML to a file
    with open("output_pacs028.xml", "w") as f:
        f.write(combined_xml)
    
    print("\nCombined XML saved to output_pacs028.xml")


if __name__ == "__main__":
    main()
