# This file was auto-generated by Fern from our API Definition.

import typing

from .environment import CandidApiEnvironment
from .resources.auth.client import AsyncAuthClient, AuthClient
from .resources.billing_notes.client import AsyncBillingNotesClient, BillingNotesClient
from .resources.encounters.client import AsyncEncountersClient, EncountersClient
from .resources.expected_network_status.client import AsyncExpectedNetworkStatusClient, ExpectedNetworkStatusClient
from .resources.guarantor.client import AsyncGuarantorClient, GuarantorClient
from .resources.payers.client import AsyncPayersClient, PayersClient
from .resources.tasks.client import AsyncTasksClient, TasksClient


class CandidApi:
    def __init__(
        self, *, environment: CandidApiEnvironment = CandidApiEnvironment.PRODUCTION, token: typing.Optional[str] = None
    ):
        self._environment = environment
        self._token = token
        self.auth = AuthClient(environment=self._environment, token=self._token)
        self.encounters = EncountersClient(environment=self._environment, token=self._token)
        self.guarantor = GuarantorClient(environment=self._environment, token=self._token)
        self.tasks = TasksClient(environment=self._environment, token=self._token)
        self.billing_notes = BillingNotesClient(environment=self._environment, token=self._token)
        self.expected_network_status = ExpectedNetworkStatusClient(environment=self._environment, token=self._token)
        self.payers = PayersClient(environment=self._environment, token=self._token)


class AsyncCandidApi:
    def __init__(
        self, *, environment: CandidApiEnvironment = CandidApiEnvironment.PRODUCTION, token: typing.Optional[str] = None
    ):
        self._environment = environment
        self._token = token
        self.auth = AsyncAuthClient(environment=self._environment, token=self._token)
        self.encounters = AsyncEncountersClient(environment=self._environment, token=self._token)
        self.guarantor = AsyncGuarantorClient(environment=self._environment, token=self._token)
        self.tasks = AsyncTasksClient(environment=self._environment, token=self._token)
        self.billing_notes = AsyncBillingNotesClient(environment=self._environment, token=self._token)
        self.expected_network_status = AsyncExpectedNetworkStatusClient(
            environment=self._environment, token=self._token
        )
        self.payers = AsyncPayersClient(environment=self._environment, token=self._token)
