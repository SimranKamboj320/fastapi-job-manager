from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.services.analytics_service import get_user_analytics

router = APIRouter(tags=["Analytics"])


@router.get("/analytics")
def analytics(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_user_analytics(db, current_user.id)