# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import uuid4

from miso20022.common import (
    PstlAdr, ClrSysId, ClrSysMmbId, FinInstnId,
    InstgAgt, InstdAgt, GrpHdr, OrgnlGrpInf
)

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
        payload: Dict[str, Any]
    ) -> "Document":
        """
        Create a payment status request document from payload data.
        
        Args:
            payload: A dictionary containing the payload data
            
        Returns:
            Document: A PACS.028 document
        """
        try:
            # Extract fedWireMessage data
            fed_wire_message = payload["fedWireMessage"]
            input_message_data = fed_wire_message["inputMessageAccountabilityData"]
            
            # Extract message ID components
            input_cycle_date = input_message_data["inputCycleDate"]
            input_source = input_message_data["inputSource"]
            input_sequence_number = input_message_data["inputSequenceNumber"]
            
            # Construct message ID
            msg_id = f"{input_cycle_date}{input_source}{input_sequence_number}"
            
            # Get pacs.028 specific fields
            original_msg_id = payload["original_msg_id"]
            original_msg_nm_id = payload["original_msg_nm_id"]
            original_creation_datetime = payload.get("original_creation_datetime")
            
            # Get optional fields
            original_instr_id = payload.get("original_instr_id")
            original_end_to_end_id = payload.get("original_end_to_end_id")
            original_uetr = payload.get("original_uetr")
            
            # Get sender/receiver information
            sender_info = fed_wire_message["senderDepositoryInstitution"]
            receiver_info = fed_wire_message["receiverDepositoryInstitution"]
            instg_agt_id = sender_info["senderABANumber"]
            instd_agt_id = receiver_info["receiverABANumber"]
                
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
        except KeyError as e:
            raise ValueError(f"Missing required key in payload: {e}")
