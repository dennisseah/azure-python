from typing import Any

from pydantic import BaseModel, ConfigDict


class OriginalResource(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    type: str
    tenantId: str
    kind: str
    location: str
    resourceGroup: str
    subscriptionId: str
    managedBy: str
    plan: dict[str, Any] | None
    properties: dict[str, Any]
    sku: dict[str, Any] | None = None
    tags: dict[str, Any] | None = None
    identity: dict[str, Any] | None = None
    zones: list[str] | None = None

    @property
    def resource_group(self) -> str:
        parts = self.id.split("/")
        return "/".join(parts[0:5])

    @property
    def resource_group_name(self) -> str:
        return self.resourceGroup

    @property
    def resource_provider_namespace(self) -> str:
        parts = self.id.split("/")
        idx = parts.index("providers")
        return parts[idx + 1]

    @property
    def resource_type(self) -> str:
        parts = self.type.split("/")
        return parts[1]

    @property
    def resource_name(self) -> str:
        return self.name
