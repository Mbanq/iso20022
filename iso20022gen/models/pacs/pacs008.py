# pacs008.py

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from random import choices
from string import ascii_letters, digits
from typing import Any, Dict, List, Optional
from uuid import uuid4


@dataclass
class ClrSysId:
    Cd: str = "USABA"

@dataclass
class PstlAdr:
    AdrLine: List[str]

@dataclass
class ClrSysMmbId:
    ClrSysId: ClrSysId
    MmbId: str


@dataclass
class FinInstnId:
    ClrSysMmbId: ClrSysMmbId
    Nm: Optional[str] = None
    PstlAdr: Optional[PstlAdr] = None


@dataclass
class InstgAgt:
    FinInstnId: FinInstnId


@dataclass
class InstdAgt:
    FinInstnId: FinInstnId


@dataclass
class Othr:
    Id: str


@dataclass
class IdAcct:
    Othr: Othr


@dataclass
class DbtrAcct:
    Id: IdAcct


@dataclass
class CdtrAcct:
    Id: IdAcct



@dataclass
class Dbtr:
    Nm: str
    PstlAdr: PstlAdr


@dataclass
class Cdtr:
    Nm: str
    PstlAdr: PstlAdr


@dataclass
class DbtrAgt:
    FinInstnId: FinInstnId


@dataclass
class CdtrAgt:
    FinInstnId: FinInstnId


@dataclass
class PmtId:
    EndToEndId: str
    UETR: str


@dataclass
class LclInstrm:
    Prtry: str = "CTRC"


@dataclass
class PmtTpInf:
    LclInstrm: LclInstrm


@dataclass
class SttlmInf:
    SttlmMtd: str = "CLRG"
    ClrSys: Dict[str, Any] = field(default_factory=lambda: {"Cd": "FDW"})


@dataclass
class GrpHdr:
    MsgId: str
    CreDtTm: str
    NbOfTxs: str
    SttlmInf: SttlmInf


@dataclass
class CdtTrfTxInf:
    PmtId: PmtId
    PmtTpInf: PmtTpInf
    IntrBkSttlmAmt: Dict[str, Any]
    IntrBkSttlmDt: str
    InstdAmt: Dict[str, Any]
    ChrgBr: str
    InstgAgt: InstgAgt
    InstdAgt: InstdAgt
    Dbtr: Dbtr
    DbtrAcct: DbtrAcct
    DbtrAgt: DbtrAgt
    CdtrAgt: CdtrAgt
    Cdtr: Cdtr
    CdtrAcct: CdtrAcct
    # Now the one default‐valued field goes last:



@dataclass
class FIToFICstmrCdtTrf:
    GrpHdr: GrpHdr
    CdtTrfTxInf: CdtTrfTxInf

@dataclass
class Document:
    FIToFICstmrCdtTrf: FIToFICstmrCdtTrf
    @classmethod
    def from_payload(cls, payload: Dict[str, Any]) -> "Document":
        msg = payload["fedWireMessage"]
        imad = msg["inputMessageAccountabilityData"]

        # Build message ID
        message_id = f"{imad['inputCycleDate']}{imad['inputSource']}{imad['inputSequenceNumber']}"

        # Generate random EndToEndId
        prefix = "MEtoEID"
        rand = ''.join(choices(ascii_letters + digits, k=15 - len(prefix)))
        end_to_end = prefix + rand
        uetr = str(uuid4())

        # Convert amount cents → dollars
        amt = float(msg["amount"]["amount"]) / 100
        ccy_amt = {"@Ccy": msg["amount"].get("currency", "USD"), "#text": str(amt)}

        # Format settlement date
        sttlm_dt = datetime.strptime(imad["inputCycleDate"], "%Y%m%d").strftime("%Y-%m-%d")

        # Helper for address lines
        def adr_lines(personal: Dict[str, Any]) -> List[str]:
            lines = []
            for key in ("addressLineOne", "addressLineTwo", "addressLineThree"):
                val = personal["address"].get(key, "").replace("NA", "").strip()
                if val:
                    lines.append(val[:35])
            return lines

        # Build all submodels
        grp_hdr = GrpHdr(
            MsgId=message_id,
            CreDtTm=datetime.now(timezone.utc).isoformat(),
            NbOfTxs="1",
            SttlmInf=SttlmInf()
        )

        cdt = CdtTrfTxInf(
            PmtId=PmtId(EndToEndId=end_to_end, UETR=uetr),
            PmtTpInf=PmtTpInf(LclInstrm=LclInstrm()),
            IntrBkSttlmAmt=ccy_amt,
            IntrBkSttlmDt=sttlm_dt,
            InstdAmt=ccy_amt,
            ChrgBr="SLEV",
            InstgAgt=InstgAgt(
                FinInstnId=FinInstnId(
                    ClrSysMmbId=ClrSysMmbId(ClrSysId(), msg["senderDepositoryInstitution"]["senderABANumber"]),
                )
            ),
            InstdAgt=InstdAgt(
                FinInstnId=FinInstnId(
                    ClrSysMmbId=ClrSysMmbId(
                        ClrSysId(),
                        msg["receiverDepositoryInstitution"]["receiverABANumber"]
                    )
                )
            ),
            Dbtr=Dbtr(
                Nm=msg["originator"]["personal"]["name"],
                PstlAdr=PstlAdr(AdrLine=adr_lines(msg["originator"]["personal"]))
            ),
            DbtrAcct=DbtrAcct(
                Id=IdAcct(Othr=Othr(Id=msg["originator"]["personal"]["identifier"]))
            ),
            DbtrAgt=DbtrAgt(
                FinInstnId=FinInstnId(
                    ClrSysMmbId=ClrSysMmbId(ClrSysId(), msg["senderDepositoryInstitution"]["senderABANumber"]),
                    Nm="vamsi",
                    PstlAdr=PstlAdr(AdrLine=adr_lines(msg["originator"]["personal"]))
                )
            ),
            CdtrAgt=CdtrAgt(
                FinInstnId=FinInstnId(
                    ClrSysMmbId=ClrSysMmbId(ClrSysId(), msg["senderDepositoryInstitution"]["senderABANumber"]),
                    Nm="vamsi",
                    PstlAdr=PstlAdr(AdrLine=adr_lines(msg["originator"]["personal"]))
                )
            ),
            Cdtr=Cdtr(
                Nm=msg["beneficiary"]["personal"]["name"],
                PstlAdr=PstlAdr(AdrLine=adr_lines(msg["beneficiary"]["personal"]))
            ),
            CdtrAcct=CdtrAcct(
                Id=IdAcct(Othr=Othr(Id=msg["beneficiary"]["personal"]["identifier"]))
            )
        )

        return cls(FIToFICstmrCdtTrf=FIToFICstmrCdtTrf(GrpHdr=grp_hdr, CdtTrfTxInf=cdt))
