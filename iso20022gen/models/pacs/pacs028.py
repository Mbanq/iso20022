# pacs028.py

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4

from iso20022gen.models.common import (
    PstlAdr, ClrSysId, ClrSysMmbId, FinInstnId,
    InstgAgt, InstdAgt, GrpHdr
)


@dataclass
class OrgnlGrpInf:
    """Original group information."""
    OrgnlMsgId: str
    OrgnlMsgNmId: str
    OrgnlCreDtTm: str


@dataclass
class TxInf:
    """Transaction information."""
    OrgnlGrpInf: OrgnlGrpInf
    OrgnlInstrId: Optional[str] = None
    OrgnlEndToEndId: Optional[str] = None
    OrgnlUETR: Optional[str] = None
    InstgAgt: Optional[InstgAgt] = None
    InstdAgt: Optional[InstdAgt] = None


@dataclass
class FIToFIPmtStsReq:
    """Financial Institution to Financial Institution Payment Status Request."""
    GrpHdr: GrpHdr
    TxInf: TxInf


@dataclass
class Document:
    """PACS.028 document."""
    FIToFIPmtStsReq: FIToFIPmtStsReq

    def to_dict(self) -> Dict[str, Any]:
        """Convert this model to a dictionary representation for XML generation."""
        return {
            "Document": {
                "@xmlns:pacs": "urn:iso:std:iso:20022:tech:xsd:pacs.028.001.03",
                **asdict(self)
            }
        }

    @classmethod
    def from_payload(
        cls,
        msg_id: str,
        original_msg_id: str,
        original_msg_nm_id: str = "pacs.008.001.08",
        original_creation_datetime: Optional[str] = None,
        original_instr_id: Optional[str] = None,
        original_end_to_end_id: Optional[str] = None,
        original_uetr: Optional[str] = None,
        instg_agt_id: Optional[str] = None,
        instd_agt_id: Optional[str] = None
    ) -> "Document":
        """
        Create a payment status request document from payload data.
        
        Args:
            msg_id: Message ID for this request
            original_msg_id: Original message ID being queried
            original_msg_nm_id: Original message type (default: pacs.008.001.08)
            original_creation_datetime: Original message creation time (ISO format)
            original_instr_id: Original instruction ID
            original_end_to_end_id: Original end-to-end ID
            original_uetr: Original UETR
            instg_agt_id: Instructing agent ID (ABA number)
            instd_agt_id: Instructed agent ID (ABA number)
            
        Returns:
            Document: A PACS.028 document
        """
        # Set default creation time to now if not provided
        if not original_creation_datetime:
            original_creation_datetime = datetime.now(timezone.utc).isoformat()
            
        # Create group header
        grp_hdr = GrpHdr(
            MsgId=msg_id,
            CreDtTm=datetime.now(timezone.utc).isoformat(),
            NbOfTxs=None, # Not needed for PACS.028
            SttlmInf=None  # Not needed for PACS.028
        )
        
        # Create original group info
        orgn_grp_inf = OrgnlGrpInf(
            OrgnlMsgId=original_msg_id,
            OrgnlMsgNmId=original_msg_nm_id,
            OrgnlCreDtTm=original_creation_datetime
        )
        
        # Create transaction info
        tx_inf = TxInf(
            OrgnlGrpInf=orgn_grp_inf,
            OrgnlInstrId=original_instr_id,
            OrgnlEndToEndId=original_end_to_end_id,
            OrgnlUETR=original_uetr
        )
        
        # Add instructing agent if provided
        if instg_agt_id:
            tx_inf.InstgAgt = InstgAgt(
                FinInstnId=FinInstnId(
                    ClrSysMmbId=ClrSysMmbId(
                        ClrSysId=ClrSysId(),
                        MmbId=instg_agt_id
                    )
                )
            )
            
        # Add instructed agent if provided
        if instd_agt_id:
            tx_inf.InstdAgt = InstdAgt(
                FinInstnId=FinInstnId(
                    ClrSysMmbId=ClrSysMmbId(
                        ClrSysId=ClrSysId(),
                        MmbId=instd_agt_id
                    )
                )
            )
        
        # Create FIToFIPmtStsReq
        fi_to_fi_pmt_sts_req = FIToFIPmtStsReq(
            GrpHdr=grp_hdr,
            TxInf=tx_inf
        )
        
        return cls(FIToFIPmtStsReq=fi_to_fi_pmt_sts_req)
