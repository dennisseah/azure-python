from typing import Literal

from pydantic import ConfigDict

from azure_python.models.original_resource import OriginalResource


class OriginalResourceActivity(OriginalResource):
    model_config = ConfigDict(frozen=True)

    res_id: str
    res_name: str
    action_type: Literal["Create", "Update", "Delete", "Compliance"]
    timestamp: str

    @property
    def resource_group(self) -> str:
        parts = self.res_id.split("/")
        return "/".join(parts[0:5])

    @property
    def resource_group_name(self) -> str:
        return self.res_id.split("/")[4]
