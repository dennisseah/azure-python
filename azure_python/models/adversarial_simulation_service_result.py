from typing import Any

from pydantic import BaseModel


class AdversarialSimulationServiceResult(BaseModel):
    simulator_name: str
    category: str | None = None
    query: str | None
    response: str | None = None

    @classmethod
    def parse(
        cls, simulator_name: str, output: dict[str, Any] | str
    ) -> "AdversarialSimulationServiceResult":
        if isinstance(output, str):
            return AdversarialSimulationServiceResult(
                simulator_name=simulator_name,
                category=output,
                query=None,
                response=None,
            )

        messages = output["messages"]
        return AdversarialSimulationServiceResult(
            simulator_name=simulator_name,
            category=output["template_parameters"].get("category", "regular"),
            query=messages[0]["content"],
            response=messages[1]["content"] if len(messages) > 1 else None,
        )
