from enum import Enum


class FlowModuleValue2Type7Type(str, Enum):
    POSTGRESQL = "postgresql"

    def __str__(self) -> str:
        return str(self.value)
