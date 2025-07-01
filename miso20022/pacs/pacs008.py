# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from random import choices
from string import ascii_letters, digits
from typing import Any, Dict, List, Optional
from uuid import uuid4

from miso20022.common import *


@dataclass
class CdtTrfTxInf:
    """Credit transfer transaction information."""
    PmtId: Optional[PmtId] = None
    PmtTpInf: Optional[PmtTpInf] = None
    IntrBkSttlmAmt: Optional[Dict[str, Any]] = None
    IntrBkSttlmDt: Optional[str] = None
    InstdAmt: Optional[Dict[str, Any]] = None
    ChrgBr: Optional[str] = None
    InstgAgt: Optional[InstgAgt] = None
    InstdAgt: Optional[InstdAgt] = None
    Dbtr: Optional[Dbtr] = None
    DbtrAcct: Optional[DbtrAcct] = None
    DbtrAgt: Optional[DbtrAgt] = None
    CdtrAgt: Optional[CdtrAgt] = None
    Cdtr: Optional[Cdtr] = None
    CdtrAcct: Optional[CdtrAcct] = None

    def __post_init__(self):
        """Validate that required fields are not None."""
        required_fields = [
            'PmtId', 'PmtTpInf', 'IntrBkSttlmAmt', 'IntrBkSttlmDt', 'InstdAmt',
            'ChrgBr', 'InstgAgt', 'InstdAgt', 'Dbtr', 'DbtrAgt', 'CdtrAgt', 'Cdtr'
        ]
        for field_name in required_fields:
            if getattr(self, field_name) is None:
                raise ValueError(f"Field '{field_name}' is required for CdtTrfTxInf but was not provided.")

    @staticmethod
    def build_fin_instn_id(data):
        return FinInstnId(
            ClrSysMmbId=ClrSysMmbId(
                ClrSysId=ClrSysId(**data['ClrSysMmbId']['ClrSysId']),
                MmbId=data['ClrSysMmbId']['MmbId']
            ),
            Nm=data.get('Nm'),
            PstlAdr=PstlAdr(**data['PstlAdr']) if data.get('PstlAdr') else None
        )


@dataclass
class FIToFICstmrCdtTrf:
    """Financial institution to financial institution customer credit transfer."""
    GrpHdr: GrpHdr
    CdtTrfTxInf: CdtTrfTxInf
    
    def __post_init__(self):
        """Validate that SttlmInf is provided for PACS.008 messages."""
        if not self.GrpHdr.SttlmInf:
            raise ValueError("SttlmInf is required for PACS.008 messages")

    @classmethod
    def from_iso20022(cls, data: Dict[str, Any]) -> "CdtTrfTxInf":

        # 1. Extract CdtTrfTxInf data
        cdt_trf_tx_inf_data = data['FedwireFundsOutgoing']['FedwireFundsOutgoingMessage']['FedwireFundsCustomerCreditTransfer']['Document']['FIToFICstmrCdtTrf']['CdtTrfTxInf']
        grp_hdr_data = data['FedwireFundsOutgoing']['FedwireFundsOutgoingMessage']['FedwireFundsCustomerCreditTransfer']['Document']['FIToFICstmrCdtTrf']['GrpHdr']

        # 2. Instantiate the CdtTrfTxInf data class with optional DbtrAcct and CdtrAcct
        grp_hdr_data = GrpHdr(**grp_hdr_data)
        cdt_trf_tx_inf = {
            'PmtId': PmtId(**cdt_trf_tx_inf_data['PmtId']),
            'PmtTpInf': PmtTpInf(LclInstrm=LclInstrm(**cdt_trf_tx_inf_data['PmtTpInf']['LclInstrm'])),
            'IntrBkSttlmAmt': {
                '@Ccy': cdt_trf_tx_inf_data['IntrBkSttlmAmt']['@attributes']['Ccy'],
                '#text': str(cdt_trf_tx_inf_data['IntrBkSttlmAmt']['#text']).replace('.', '')
            },
            'IntrBkSttlmDt': cdt_trf_tx_inf_data['IntrBkSttlmDt'],
            'InstdAmt': {
                '@Ccy': cdt_trf_tx_inf_data['InstdAmt']['@attributes']['Ccy'],
                '#text': str(cdt_trf_tx_inf_data['InstdAmt']['#text']).replace('.', '')
            },
            'ChrgBr': cdt_trf_tx_inf_data['ChrgBr'],
            'InstgAgt': InstgAgt(FinInstnId=CdtTrfTxInf.build_fin_instn_id(cdt_trf_tx_inf_data['InstgAgt']['FinInstnId'])),
            'InstdAgt': InstdAgt(FinInstnId=CdtTrfTxInf.build_fin_instn_id(cdt_trf_tx_inf_data['InstdAgt']['FinInstnId'])),
            'Dbtr': Dbtr(Nm=cdt_trf_tx_inf_data['Dbtr']['Nm'], PstlAdr=PstlAdr(**cdt_trf_tx_inf_data['Dbtr']['PstlAdr'])),
            'DbtrAcct': DbtrAcct(Id=IdAcct(Othr=Othr(**cdt_trf_tx_inf_data['DbtrAcct']['Id']['Othr']))) if 'DbtrAcct' in cdt_trf_tx_inf_data and 'Id' in cdt_trf_tx_inf_data['DbtrAcct'] and 'Othr' in cdt_trf_tx_inf_data['DbtrAcct']['Id'] else None,
            'DbtrAgt': DbtrAgt(FinInstnId=CdtTrfTxInf.build_fin_instn_id(cdt_trf_tx_inf_data['DbtrAgt']['FinInstnId'])),
            'CdtrAgt': CdtrAgt(FinInstnId=CdtTrfTxInf.build_fin_instn_id(cdt_trf_tx_inf_data['CdtrAgt']['FinInstnId'])),
            'Cdtr': Cdtr(Nm=cdt_trf_tx_inf_data['Cdtr']['Nm'], PstlAdr=PstlAdr(**cdt_trf_tx_inf_data['Cdtr']['PstlAdr'])),
            'CdtrAcct': CdtrAcct(Id=IdAcct(Othr=Othr(**cdt_trf_tx_inf_data['CdtrAcct']['Id']['Othr']))) if 'CdtrAcct' in cdt_trf_tx_inf_data and 'Id' in cdt_trf_tx_inf_data['CdtrAcct'] and 'Othr' in cdt_trf_tx_inf_data['CdtrAcct']['Id'] else None,
        }
        
        cdt_trf_tx_inf = CdtTrfTxInf(**cdt_trf_tx_inf)

        return grp_hdr_data, cdt_trf_tx_inf


@dataclass
class Document:
    """PACS.008 document."""
    FIToFICstmrCdtTrf: FIToFICstmrCdtTrf

    def to_dict(self) -> Dict[str, Any]:
        """Convert this model to a dictionary representation for XML generation."""
        return {
            "Document": {
                "@xmlns:pacs": "urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08",
                **asdict(self)
            }
        }

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
                    if len(val) > 32:
                        raise ValueError(f"Address line '{key}' ('{val}') exceeds 32 characters.")
                    lines.append(val)
            return lines

        # Build all submodels
        grp_hdr = GrpHdr(
            MsgId=message_id,
            CreDtTm=datetime.now(timezone.utc).isoformat(),
            #Need to change this and make it dynamic
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
                    Nm=msg["senderDepositoryInstitution"]["senderShortName"],
                    PstlAdr=PstlAdr(AdrLine=adr_lines(msg["originator"]["personal"]))
                )
            ),
            CdtrAgt=CdtrAgt(
                FinInstnId=FinInstnId(
                    ClrSysMmbId=ClrSysMmbId(ClrSysId(), msg["receiverDepositoryInstitution"]["receiverABANumber"]),
                    Nm=msg["receiverDepositoryInstitution"]["receiverShortName"],
                    PstlAdr=PstlAdr(AdrLine=adr_lines(msg["beneficiary"]["personal"]))
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

    
    
