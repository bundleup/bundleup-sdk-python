from typing import Any, Dict, Optional, cast

from .base import Base
from .types import CompaniesResponse, ContactsResponse


class CRM(Base):
    def companies(self, params: Optional[Dict[str, Any]] = None) -> CompaniesResponse:
        """
        List CRM companies
        """
        url = self._build_url("crm/companies")
        response = self._connection.get(url, params=params)

        if not response.ok:
            raise Exception(f"Failed to fetch crm/companies: {response.status_code}")

        return cast(CompaniesResponse, response.json())

    def contacts(self, params: Optional[Dict[str, Any]] = None) -> ContactsResponse:
        """
        List CRM contacts
        """
        url = self._build_url("crm/contacts")
        response = self._connection.get(url, params=params)

        if not response.ok:
            raise Exception(f"Failed to fetch crm/contacts: {response.status_code}")

        return cast(ContactsResponse, response.json())
