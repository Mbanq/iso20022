# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class EvtInf:
    EvtCd: str
    EvtParam: str
    EvtTm: str



@dataclass
class SysEvtNtfctn:
    EvtInf: EvtInf


@dataclass
class Admi004Document:
    SysEvtNtfctn: SysEvtNtfctn

    def to_dict(self, message_code: str) -> Dict[str, Any]:
        """Convert this model to a dictionary representation for XML generation."""
        evt_inf_dict = asdict(self.SysEvtNtfctn.EvtInf)
        prefixed_evt_inf = {f'admi:{k}': v for k, v in evt_inf_dict.items()}

        return {
            'admi:Document': {
                '@xmlns:admi': message_code,
                'admi:SysEvtNtfctn': {
                    'admi:EvtInf': prefixed_evt_inf
                }
            }
        }

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]) -> "Admi004Document":
        """Create a Document instance from a payload dictionary."""
        doc_data = payload.get('Document', {})
        sys_evt_data = doc_data.get('SystemEvtNtfctn') or doc_data.get('SysEvtNtfctn')
        if not sys_evt_data:
            raise ValueError("Payload is missing required 'SystemEvtNtfctn' or 'SysEvtNtfctn' data")

        evt_inf_data = sys_evt_data.get('EvtInf', {})
        if not evt_inf_data:
            raise ValueError("Payload is missing required 'EvtInf' data")

        return cls(
            SysEvtNtfctn=SysEvtNtfctn(
                EvtInf=EvtInf(**evt_inf_data)
            )
        )
