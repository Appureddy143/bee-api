from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
import database
import auth

router = APIRouter(prefix="/farmer", tags=["Farmer"])

@router.post("/farms", response_model=schemas.FarmResponse)
def create_farm(farm: schemas.FarmCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role != models.UserRole.FARMER:
        raise HTTPException(status_code=403, detail="Only farmers can add farms")
    
    new_farm = models.Farm(**farm.model_dump(), owner_id=current_user.id)
    db.add(new_farm)
    db.commit()
    db.refresh(new_farm)
    return new_farm

@router.get("/farms", response_model=List[schemas.FarmResponse])
def get_farms(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Farm).filter(models.Farm.owner_id == current_user.id).all()

@router.post("/spray-alerts", response_model=schemas.SprayAlertResponse)
def create_spray_alert(alert: schemas.SprayAlertCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role != models.UserRole.FARMER:
        raise HTTPException(status_code=403, detail="Only farmers can schedule spray alerts")
    
    farm = db.query(models.Farm).filter(models.Farm.id == alert.farm_id, models.Farm.owner_id == current_user.id).first()
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")

    new_alert = models.SprayAlert(**alert.model_dump())
    db.add(new_alert)
    
    # Generate Notification for the alert
    new_notif = models.Notification(
        user_id=current_user.id,
        title="Spray Alert Scheduled",
        message=f"You scheduled a spray alert for {alert.pesticide_type} on Farm ID {alert.farm_id}."
    )
    db.add(new_notif)
    
    db.commit()
    db.refresh(new_alert)

    # TODO: Trigger FCM to nearby beekeepers based on radius
    
    return new_alert

@router.get("/spray-alerts", response_model=List[schemas.SprayAlertResponse])
def get_spray_alerts(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.SprayAlert).all()
