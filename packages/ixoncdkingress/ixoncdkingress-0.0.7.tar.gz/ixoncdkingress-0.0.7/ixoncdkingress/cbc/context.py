"""
Context.
"""
from typing import Any, Dict, Optional, Set

from ixoncdkingress.cbc.api_client import ApiClient

class CbcIxapiResource:
    """
    Describes an IXAPI resource.
    """
    public_id: str
    name: str
    custom_properties: Dict[str, Any]
    permissions: Optional[Set[str]]

    def __init__(
            self,
            public_id: str,
            name: str,
            custom_properties: Dict[str, Any],
            permissions: Optional[Set[str]]
        ) -> None:
        self.public_id = public_id
        self.name = name
        self.custom_properties = custom_properties
        self.permissions = permissions

    def __repr__(self) -> str:
        return (
            '<CbcResource'
            f' public_id={self.public_id},'
            f' name={self.name},'
            f' custom_properties={repr(self.custom_properties)},'
            f' permissions={repr(self.permissions)},'
            f'>'
        )

class CbcContext:
    """
    The context for a backend component.
    """
    config: Dict[str, str]

    api_client: ApiClient

    user: Optional[CbcIxapiResource] = None

    company: Optional[CbcIxapiResource] = None

    asset: Optional[CbcIxapiResource] = None

    agent: Optional[CbcIxapiResource] = None

    @property
    def agent_or_asset(self) -> CbcIxapiResource:
        """
        Return either an Agent or an Asset resource, depending on what's available. If both are
        available in the context, returns the Asset resource.
        """
        if self.asset:
            return self.asset

        assert self.agent
        return self.agent

    def __init__(
            self,
            config: Dict[str, str],
            api_client: ApiClient,
            user: Optional[CbcIxapiResource] = None,
            company: Optional[CbcIxapiResource] = None,
            asset: Optional[CbcIxapiResource] = None,
            agent: Optional[CbcIxapiResource] = None,
            **kwargs: Any
        ) -> None:
        del kwargs

        self.config = config
        self.api_client = api_client
        self.user = user
        self.company = company
        self.asset = asset
        self.agent = agent

    def __repr__(self) -> str:
        return (
            f'<CbcContext'
            f' config={repr(self.config)},'
            f' api_client={repr(self.api_client)},'
            f' user={repr(self.user)},'
            f' company={repr(self.company)},'
            f' asset={repr(self.asset)},'
            f' agent={repr(self.agent)},'
            f'>'
        )
