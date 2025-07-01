# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Dict, Any, Tuple


@dataclass
class ClrSysMmbId:
    MmbId: str


@dataclass
class FinInstnId:
    ClrSysMmbId: ClrSysMmbId


@dataclass
class FIId:
    FinInstnId: FinInstnId


@dataclass
class Fr:
    FIId: FIId


@dataclass
class To:
    FIId: FIId


@dataclass
class MktPrctc:
    Regy: str
    Id: str


@dataclass
class AppHdr:
    Fr: Fr
    To: To
    BizMsgIdr: str
    MsgDefIdr: str
    BizSvc: str
    MktPrctc: MktPrctc
    CreDt: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert this model to a dictionary representation for XML generation."""
        return {
            "AppHdr": {
                "@xmlns:head": "urn:iso:std:iso:20022:tech:xsd:head.001.001.03",
                **asdict(self)
            }
        }

    @classmethod
    def from_payload(
            cls,
            environment,
            fed_aba,
            message_code,
            payload: Dict[str, Any]
    ) -> "AppHdr":
        """Create an AppHdr instance from a payload dictionary.

        Args:
            environment: The environment for the message, either "TEST" or "PROD".
            fed_aba: The Fed ABA number for the receiving institution.
            message_code: The ISO20022 message code (e.g., urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08).
            payload: The payload data as a dictionary.

        Returns:
            An AppHdr instance.
        """
        fedwire_message = payload["fedWireMessage"]
        msg_data = fedwire_message["inputMessageAccountabilityData"]
        message_id = (
            f"{msg_data['inputCycleDate']}"
            f"{msg_data['inputSource']}"
            f"{msg_data['inputSequenceNumber']}"
        )

        sender_aba = fedwire_message["senderDepositoryInstitution"]["senderABANumber"]
        receiver_aba = fed_aba

        # Extract only the message type from the full message code
        msg_def_idr = message_code.split(':')[-1]

        return cls(
            Fr=Fr(
                FIId=FIId(
                    FinInstnId=FinInstnId(
                        ClrSysMmbId=ClrSysMmbId(MmbId=sender_aba)
                    )
                )
            ),
            To=To(
                FIId=FIId(
                    FinInstnId=FinInstnId(
                        ClrSysMmbId=ClrSysMmbId(MmbId=receiver_aba)
                    )
                )
            ),
            BizMsgIdr=message_id,
            MsgDefIdr=msg_def_idr,
            BizSvc=environment,
            MktPrctc=MktPrctc(
                Regy="www2.swift.com/mystandards/#/group/Federal_Reserve_Financial_Services/Fedwire_Funds_Service",
                Id="frb.fedwire.01"
            ),
            CreDt=datetime.now(timezone.utc).isoformat(),
        )

    @classmethod
    def from_iso20022(cls, data: Dict[str, Any],message_code)-> "AppHdr":

        # 1. Extract AppHdr data
        if message_code == "urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08":
            app_hdr_data = data['FedwireFundsOutgoing']['FedwireFundsOutgoingMessage']['FedwireFundsCustomerCreditTransfer']['AppHdr']
        elif message_code == "urn:iso:std:iso:20022:tech:xsd:pacs.002.001.10":
            app_hdr_data = data['FedwireFundsOutgoing']['FedwireFundsOutgoingMessage']['FedwireFundsPaymentStatus']['AppHdr']

        # 2. Instantiate the AppHdr data class
        app_hdr = AppHdr(
            Fr=Fr(FIId=FIId(FinInstnId=FinInstnId(ClrSysMmbId=ClrSysMmbId(**app_hdr_data['Fr']['FIId']['FinInstnId']['ClrSysMmbId'])))),
            To=To(FIId=FIId(FinInstnId=FinInstnId(ClrSysMmbId=ClrSysMmbId(**app_hdr_data['To']['FIId']['FinInstnId']['ClrSysMmbId'])))),
            BizMsgIdr=app_hdr_data['BizMsgIdr'],
            MsgDefIdr=app_hdr_data['MsgDefIdr'],
            BizSvc=app_hdr_data['BizSvc'],
            MktPrctc=MktPrctc(**app_hdr_data['MktPrctc']),
            CreDt=app_hdr_data['CreDt']
        )

        return app_hdr