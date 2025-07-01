# SPDX-License-Identifier: Apache-2.0

"""Common customer-related models used across ISO20022 messages."""

from dataclasses import dataclass
from typing import List, Optional

from miso20022.common.account import IdAcct


@dataclass
class PstlAdr:
    """Postal address information."""
    StrtNm: Optional[str] = None
    BldgNb: Optional[str] = None
    BldgNm: Optional[str] = None  # Added to handle Building Name field
    Flr: Optional[str] = None
    Room: Optional[str] = None
    PstCd: Optional[str] = None
    PstBx: Optional[str] = None  # Added to handle PostBox field
    TwnNm: Optional[str] = None
    TwnLctnNm: Optional[str] = None  # Added to handle Town Location Name field
    DstrctNm: Optional[str] = None  # Added to handle District Name field
    CtrySubDvsn: Optional[str] = None
    Ctry: Optional[str] = None
    AdrLine: Optional[List[str]] = None
    Dept: Optional[str] = None  # Added to handle Department field
    SubDept: Optional[str] = None  # Added to handle SubDepartment field


@dataclass
class ClrSysId:
    """Clearing system identification."""
    Cd: str = "USABA"


@dataclass
class ClrSysMmbId:
    """Clearing system member identification."""
    ClrSysId: ClrSysId
    MmbId: str


@dataclass
class FinInstnId:
    """Financial institution identification."""
    ClrSysMmbId: ClrSysMmbId
    Nm: Optional[str] = None
    PstlAdr: Optional[PstlAdr] = None


@dataclass
class InstgAgt:
    """Instructing agent."""
    FinInstnId: FinInstnId


@dataclass
class InstdAgt:
    """Instructed agent."""
    FinInstnId: FinInstnId


@dataclass
class DbtrAcct:
    """Debtor account."""
    Id: IdAcct


@dataclass
class CdtrAcct:
    """Creditor account."""
    Id: IdAcct


@dataclass
class Dbtr:
    """Debtor party."""
    Nm: str
    PstlAdr: PstlAdr


@dataclass
class Cdtr:
    """Creditor party."""
    Nm: str
    PstlAdr: PstlAdr


@dataclass
class DbtrAgt:
    """Debtor agent."""
    FinInstnId: FinInstnId


@dataclass
class CdtrAgt:
    """Creditor agent."""
    FinInstnId: FinInstnId
