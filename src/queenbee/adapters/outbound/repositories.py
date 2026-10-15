
"""Dépôts d'incidents en mémoire et SQLite."""

import sqlite3
from uuid import UUID

from queenbee.domain.model import (
    Alert,
    DomainError,
    Incident,
    IncidentStatus,
    Severity,
)


class InMemoryIncidentRepository:
    """Stocke les incidents en mémoire."""

    def __init__(self) -> None:
        self.incidents: list[Incident] = []

    def save(self, incident: Incident) -> None:
        """Ajoute ou met à jour un incident."""

        for index, existing in enumerate(self.incidents):
            if existing.id == incident.id:
                self.incidents[index] = incident
                return

        self.incidents.append(incident)

    def get(self, incident_id: UUID) -> Incident:
        """Retrouve un incident par son identifiant."""

        for incident in self.incidents:
            if incident.id == incident_id:
                return incident

        raise DomainError("Incident introuvable")

    def get_by_id(self, incident_id: str) -> Incident | None:
        """Recherche un incident à partir d'un identifiant texte."""

        try:
            return self.get(UUID(incident_id))
        except (ValueError, DomainError):
            return None

    def list_all(self) -> list[Incident]:
        """Retourne tous les incidents."""

        return list(self.incidents)

    def list_open(self) -> list[Incident]:
        """Retourne les incidents ouverts."""

        return [
            incident
            for incident in self.incidents
            if incident.status is IncidentStatus.OPEN
        ]


class SqliteIncidentRepository:
    """Stocke les incidents dans SQLite."""

    def __init__(
        self,
        db_path: str | sqlite3.Connection = ":memory:",
    ) -> None:
        if isinstance(db_path, sqlite3.Connection):
            self.connection = db_path
        else:
            self.connection = sqlite3.connect(db_path)

        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS incidents (
                id TEXT PRIMARY KEY,
                rule TEXT NOT NULL,
                source_ip TEXT NOT NULL,
                severity TEXT NOT NULL,
                message TEXT NOT NULL,
                status TEXT NOT NULL
            )
            """
        )
        self.connection.commit()

    def save(self, incident: Incident) -> None:
        """Ajoute ou met à jour un incident."""

        self.connection.execute(
            """
            INSERT INTO incidents
                (id, rule, source_ip, severity, message, status)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                rule = excluded.rule,
                source_ip = excluded.source_ip,
                severity = excluded.severity,
                message = excluded.message,
                status = excluded.status
            """,
            (
                str(incident.id),
                incident.alert.rule,
                incident.alert.source_ip,
                incident.alert.severity.value,
                incident.alert.message,
                incident.status.value,
            ),
        )
        self.connection.commit()

    def get(self, incident_id: UUID) -> Incident:
        """Retrouve un incident par son identifiant."""

        row = self.connection.execute(
            """
            SELECT id, rule, source_ip, severity, message, status
            FROM incidents
            WHERE id = ?
            """,
            (str(incident_id),),
        ).fetchone()

        if row is None:
            raise DomainError("Incident introuvable")

        return self._from_row(row)

    def get_by_id(self, incident_id: str) -> Incident | None:
        """Recherche un incident à partir d'un identifiant texte."""

        try:
            return self.get(UUID(incident_id))
        except (ValueError, DomainError):
            return None

    def list_all(self) -> list[Incident]:
        """Retourne tous les incidents."""

        rows = self.connection.execute(
            """
            SELECT id, rule, source_ip, severity, message, status
            FROM incidents
            """
        ).fetchall()

        return [self._from_row(row) for row in rows]

    def list_open(self) -> list[Incident]:
        """Retourne les incidents ouverts."""

        rows = self.connection.execute(
            """
            SELECT id, rule, source_ip, severity, message, status
            FROM incidents
            WHERE status = ?
            """,
            (IncidentStatus.OPEN.value,),
        ).fetchall()

        return [self._from_row(row) for row in rows]

    @staticmethod
    def _from_row(row: tuple[str, ...]) -> Incident:
        """Reconstruit un incident depuis SQLite."""

        incident_id, rule, source_ip, severity, message, status = row

        alert = Alert(
            rule=rule,
            source_ip=source_ip,
            severity=Severity(severity),
            message=message,
        )

        return Incident(
            alert=alert,
            status=IncidentStatus(status),
            id=UUID(incident_id),
        )

