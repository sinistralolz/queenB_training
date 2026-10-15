
import sqlite3

from queenbee.domain.model import Incident


class InMemoryIncidentRepository:
    """Stocke les incidents en mémoire."""

    def __init__(self) -> None:
        self.incidents: list[Incident] = []

    def save(self, incident: Incident) -> None:
        """Enregistre un incident."""
        self.incidents.append(incident)

    def list_all(self) -> list[Incident]:
        """Retourne les incidents enregistrés."""
        return list(self.incidents)


class SqliteIncidentRepository:
    """Stocke les incidents dans une base SQLite."""

    def __init__(self, db_path: str = ":memory:") -> None:
        self.connection = sqlite3.connect(db_path)
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rule TEXT NOT NULL,
                source_ip TEXT NOT NULL,
                severity TEXT NOT NULL,
                status TEXT NOT NULL
            )
            """
        )
        self.connection.commit()

    def save(self, incident: Incident) -> None:
        """Enregistre un incident dans SQLite."""
        self.connection.execute(
            """
            INSERT INTO incidents (rule, source_ip, severity, status)
            VALUES (?, ?, ?, ?)
            """,
            (
                incident.alert.rule,
                incident.alert.source_ip,
                incident.alert.severity.value,
                incident.status.value,
            ),
        )
        self.connection.commit()
