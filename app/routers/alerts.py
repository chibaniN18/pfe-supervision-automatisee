from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from ..glpi import create_glpi_ticket

router = APIRouter(
    prefix="/alerts",
    tags=["alerts"]
)

# Créer une alerte
@router.post("/", response_model=schemas.AlertResponse)
def create_alert(alert: schemas.AlertCreate, db: Session = Depends(get_db)):
    db_alert = models.Alert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    
    # Créer un ticket GLPI si l'alerte est critique
    if alert.level == "critical":
        create_glpi_ticket(
            title=f"🚨 {alert.title}",
            description=f"{alert.description}\nSource: {alert.source}",
            urgency=5
        )
    elif alert.level == "warning":
        create_glpi_ticket(
            title=f"⚠️ {alert.title}",
            description=f"{alert.description}\nSource: {alert.source}",
            urgency=3
        )
    
    return db_alert

# Lire toutes les alertes
@router.get("/", response_model=List[schemas.AlertResponse])
def get_alerts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    alerts = db.query(models.Alert).offset(skip).limit(limit).all()
    return alerts

# Lire une alerte par ID
@router.get("/{alert_id}", response_model=schemas.AlertResponse)
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alerte non trouvée")
    return alert

# Mettre à jour une alerte
@router.put("/{alert_id}", response_model=schemas.AlertResponse)
def update_alert(alert_id: int, alert: schemas.AlertUpdate, db: Session = Depends(get_db)):
    db_alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if not db_alert:
        raise HTTPException(status_code=404, detail="Alerte non trouvée")
    for key, value in alert.dict(exclude_unset=True).items():
        setattr(db_alert, key, value)
    db.commit()
    db.refresh(db_alert)
    return db_alert

# Supprimer une alerte
@router.delete("/{alert_id}")
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    db_alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if not db_alert:
        raise HTTPException(status_code=404, detail="Alerte non trouvée")
    db.delete(db_alert)
    db.commit()
    return {"message": "Alerte supprimée avec succès"}
