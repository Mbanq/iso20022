# SPDX-License-Identifier: Apache-2.0

"""Common payment-related models used across ISO20022 messages."""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class PmtId:
    """Payment identification."""
    EndToEndId: str
    UETR: str
    InstrId: Optional[str] = None
    TxId: Optional[str] = None


@dataclass
class LclInstrm:
    """Local instrument."""
    Prtry: str = "CTRC"


@dataclass
class PmtTpInf:
    """Payment type information."""
    LclInstrm: LclInstrm


@dataclass
class SttlmInf:
    """Settlement information."""
    SttlmMtd: str = "CLRG"
    ClrSys: Dict[str, Any] = field(default_factory=lambda: {"Cd": "FDW"})


@dataclass
class GrpHdr:
    """Group header."""
    MsgId: str
    CreDtTm: str
    NbOfTxs: Optional[NbOfTxs] = None
    SttlmInf: Optional[SttlmInf] = None

@dataclass
class OrgnlGrpInf:
    """Original group information."""
    OrgnlMsgId: str
    OrgnlMsgNmId: str
    OrgnlCreDtTm: str
