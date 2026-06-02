from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from .database import Base
import enum

# Les différents niveaux d'alerte possibles
class AlertLevel(str, enum.Enum):
    info = "info"
    warning = "warning"
    critical = "critical"

# Les différents statuts d'une alerte
class AlertStatus(str, enum.Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"

# Table des alertes
class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)        # Titre de l'alerte
    description = Column(String, nullable=True)   # Description
    level = Column(Enum(AlertLevel), default=AlertLevel.info)      # Niveau
    status = Column(Enum(AlertStatus), default=AlertStatus.open)   # Statut
    source = Column(String, nullable=True)        # Source (Zabbix, etc.)
    created_at = Column(DateTime, default=func.now())  # Date de création
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
