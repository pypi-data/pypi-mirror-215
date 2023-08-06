from enum import Enum


class PostgresqlType(str, Enum):
    POSTGRESQL = "postgresql"

    def __str__(self) -> str:
        return str(self.value)
