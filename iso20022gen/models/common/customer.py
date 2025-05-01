"""Common customer-related models used across ISO20022 messages."""

from dataclasses import dataclass
from typing import List, Optional

from iso20022gen.models.common.account import IdAcct


@dataclass
class PstlAdr:
    """Postal address information."""
    AdrLine: List[str]


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
