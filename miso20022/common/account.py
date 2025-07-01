# SPDX-License-Identifier: Apache-2.0

"""Common account-related models used across ISO20022 messages."""

from dataclasses import dataclass


@dataclass
class Othr:
    """Other account identification."""
    Id: str


@dataclass
class IdAcct:
    """Account identification."""
    Othr: Othr


@dataclass
class Account:
    """Base class for accounts."""
    Id: IdAcct
