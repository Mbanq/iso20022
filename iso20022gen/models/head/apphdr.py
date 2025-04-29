# apphdr.py

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Dict, Any


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
            payload: Dict[str, Any]
    ) -> "AppHdr":
        fedwire_message = payload["fedWireMessage"]
        msg_data = fedwire_message["inputMessageAccountabilityData"]
        message_id = (
            f"{msg_data['inputCycleDate']}"
            f"{msg_data['inputSource']}"
            f"{msg_data['inputSequenceNumber']}"
        )

        sender_aba = fedwire_message["senderDepositoryInstitution"]["senderABANumber"]
        receiver_aba = fedwire_message["receiverDepositoryInstitution"]["receiverABANumber"]

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
            MsgDefIdr="pacs.008.001.08",
            BizSvc="TEST",
            MktPrctc=MktPrctc(
                Regy="www2.swift.com/mystandards/#/group/Federal_Reserve_Financial_Services/Fedwire_Funds_Service",
                Id="frb.fedwire.01"
            ),
            CreDt=datetime.now(timezone.utc).isoformat(),
        )
