# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, Optional, List
from uuid import uuid4

from miso20022.common import (
    PstlAdr, ClrSysId, ClrSysMmbId, FinInstnId,
    InstgAgt, InstdAgt, GrpHdr, OrgnlGrpInf
)

@dataclass
class Rsn:
    Prtry: str


@dataclass
class StsRsnInf:
    Rsn: Rsn
    AddtlInf: str
    

@dataclass
class TxInfAndSts:
    OrgnlGrpInf: OrgnlGrpInf
    TxSts: str
    InstgAgt: InstgAgt
    InstdAgt: InstdAgt
    StsId: Optional[str] = None
    OrgnlUETR: Optional[str] = None
    StsRsnInf: Optional[StsRsnInf] = None
    AccptncDtTm: Optional[str] = None
    FctvIntrBkSttlmDt: Optional[str] = None

    
    def __post_init__(self):
        """Validate that TxSts has one of the allowed values."""
        allowed_values = ["ACSC", "PDNG", "RJCT"]
        if self.TxSts and self.TxSts not in allowed_values:
            raise ValueError(f"TxSts must be one of {allowed_values}, got {self.TxSts}")

@dataclass
class FIToFIPmtStsRpt:
    GrpHdr: GrpHdr
    TxInfAndSts: TxInfAndSts

    @classmethod
    def from_iso20022(
        cls,
        data: Dict[str, Any]
    ) -> "FIToFIPmtStsRpt":
        
        # 1. Extract FIToFIPmtStsRpt data
        fi_to_fi_pmt_sts_rpt_data = data['FedwireFundsOutgoing']['FedwireFundsOutgoingMessage']['FedwireFundsPaymentStatus']['Document']['FIToFIPmtStsRpt']

        # 2. Instantiate the FIToFIPmtStsRpt data class
        pmt_sts_rpt = FIToFIPmtStsRpt(
            GrpHdr=GrpHdr(**fi_to_fi_pmt_sts_rpt_data['GrpHdr']),
            TxInfAndSts=TxInfAndSts(**fi_to_fi_pmt_sts_rpt_data['TxInfAndSts'])
        )
        
        return pmt_sts_rpt
   
