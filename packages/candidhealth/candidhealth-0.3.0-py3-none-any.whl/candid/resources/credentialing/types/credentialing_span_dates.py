# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import typing

import typing_extensions

from .non_required_credentialing_dates import NonRequiredCredentialingDates
from .required_credentialing_dates import RequiredCredentialingDates


class CredentialingSpanDates_RequiredDates(RequiredCredentialingDates):
    type: typing_extensions.Literal["required_dates"]

    class Config:
        frozen = True
        allow_population_by_field_name = True


class CredentialingSpanDates_NonRequiredDates(NonRequiredCredentialingDates):
    type: typing_extensions.Literal["non_required_dates"]

    class Config:
        frozen = True
        allow_population_by_field_name = True


CredentialingSpanDates = typing.Union[CredentialingSpanDates_RequiredDates, CredentialingSpanDates_NonRequiredDates]
