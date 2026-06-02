from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .models import AlertLevel, AlertStatus

# Données de base d'une alerte
class AlertBase(BaseModel):
    title: str
    description: Optional[str] = None
    level: AlertLevel = AlertLevel.info
    status: AlertStatus = AlertStatus.open
    source: Optional[str] = None

# Données pour créer une alerte
class AlertCreate(AlertBase):
    pass

# Données pour mettre à jour une alerte
class AlertUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    level: Optional[AlertLevel] = None
    status: Optional[AlertStatus] = None
    source: Optional[str] = None

# Données retournées par l'API
class AlertResponse(AlertBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
