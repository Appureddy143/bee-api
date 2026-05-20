from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models
import schemas
import database
import auth

router = APIRouter(prefix="/sos", tags=["Emergency SOS"])

@router.post("/", response_model=schemas.SosResponse)
def create_sos(sos: schemas.SosCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    new_sos = models.SosRequest(**sos.model_dump(), user_id=current_user.id)
    db.add(new_sos)
    
    # Generate Notification for the SOS alert
    new_notif = models.Notification(
        user_id=current_user.id,
        title="Emergency SOS Sent",
        message=f"You triggered an SOS alert at {sos.latitude}, {sos.longitude}."
    )
    db.add(new_notif)
    
    db.commit()
    db.refresh(new_sos)

    # TODO: Send FCM critical alert to nearby users
    print(f"SOS ALERT TRIGGERED by {current_user.name} at {sos.latitude}, {sos.longitude}")

    return new_sos
