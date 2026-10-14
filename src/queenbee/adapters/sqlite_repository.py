
import sqlite3

from queenbee.domain.model import Incident


class SQLiteIncidentRepository:
    """Enregistre les incidents dans une base SQLite."""

    def __init__(self, db_path: str = "incidents.db"):
        self.db_path = db_path

    def save(self, incident: Incident) -> None:
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS incidents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_ip TEXT NOT NULL,
                    rule TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    status TEXT NOT NULL
                )
                """
            )

            connection.execute(
                """
                INSERT INTO incidents
                (source_ip, rule, severity, status)
                VALUES (?, ?, ?, ?)
                """,
                (
                    incident.alert.source_ip,
                    incident.alert.rule,
                    incident.alert.severity.value,
                    incident.status.value,
                ),
            )
