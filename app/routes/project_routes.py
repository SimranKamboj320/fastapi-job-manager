from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.project_schema import ProjectCreate
from app.services.project_service import create_project
from app.dependencies import get_current_user

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("", status_code=201)
def create(project: ProjectCreate,
           db: Session = Depends(get_db),
           current_user=Depends(get_current_user)):

    return create_project(db, current_user.id, project)