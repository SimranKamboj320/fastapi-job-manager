from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.job_schema import JobCreate, JobResponse, StatusEnum, PriorityEnum
from app.services.job_service import (create_job, get_jobs,
    execute_job, get_job_result, delete_job)

router = APIRouter(tags=["Jobs"])

@router.post("/projects/{project_id}/jobs", response_model=JobResponse, status_code=201)
def create_job_route(
    project_id: str,
    job: JobCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return create_job(db, job, project_id, current_user.id)

@router.get("/projects/{project_id}/jobs", response_model=list[JobResponse])
def list_jobs(
    project_id: str,
    status: Optional[StatusEnum] = None,
    priority: Optional[PriorityEnum] = None,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "created_at",
    order: str = "asc",
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_jobs(db, project_id, current_user.id,
        status, priority, page, limit, sort_by, order)

@router.post("/jobs/{job_id}/execute", response_model=JobResponse)
def execute_job_route(
    job_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return execute_job(db, job_id, current_user.id)

@router.get("/jobs/{job_id}/result")
def get_job_result_route(
    job_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_job_result(db, job_id, current_user.id)

@router.delete("/jobs/{job_id}", status_code=204)
def delete_job_route(
    job_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    delete_job(db, job_id, current_user.id)