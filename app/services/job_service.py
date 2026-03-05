from sqlalchemy.orm import Session
from app.models.job import Job, JobStatus
from app.models.project import Project
from app.schemas.job_schema import JobCreate, StatusEnum, PriorityEnum
from fastapi import HTTPException
from app.services.redis_service import check_rate_limit, cache_job_result, get_cached_result
import json
import time
import random

def create_job(db: Session, job: JobCreate, project_id: str, user_id: str):

    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail={"error": "Project not found"}
        )

    if project.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail={"error": "Unauthorized access"}
        )

    new_job = Job(
        name=job.name,
        payload=json.dumps(job.payload),
        priority=job.priority,
        project_id=project_id
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    new_job.payload = json.loads(new_job.payload)

    return new_job

def get_job_by_id(db: Session, job_id: str):

    job = db.query(Job).filter(Job.id == job_id).first()

    if job and isinstance(job.payload, str):
        job.payload = json.loads(job.payload)

    return job

def get_jobs(
    db: Session,
    project_id: str,
    user_id: str,
    status: StatusEnum = None,
    priority: PriorityEnum = None,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "created_at",
    order: str = "asc"
):

    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail={"error": "Project not found"}
        )

    if project.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail={"error": "Unauthorized access"}
        )

    query = db.query(Job).filter(Job.project_id == project_id)

    if status:
        query = query.filter(Job.status == status)

    if priority:
        query = query.filter(Job.priority == priority)

    allowed_sort_fields = ["created_at", "priority"]

    if sort_by not in allowed_sort_fields:
        sort_by = "created_at"

    column = getattr(Job, sort_by)

    if order == "desc":
        query = query.order_by(column.desc())
    else:
        query = query.order_by(column.asc())

    jobs = query.offset((page - 1) * limit).limit(limit).all()

    for job in jobs:
        if isinstance(job.payload, str):
            job.payload = json.loads(job.payload)

    return jobs

def delete_job(db: Session, job_id: str, user_id: str):

    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail={"error": "Job not found"}
        )

    if job.project.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail={"error": "Unauthorized access"}
        )

    db.delete(job)
    db.commit()

    return {"message": "Job deleted successfully"}

def execute_job(db: Session, job_id: str, user_id: str):

    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail={"error": "Job not found"}
        )

    if job.project.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail={"error": "Unauthorized access"}
        )

    check_rate_limit(user_id)

    job.status = JobStatus.RUNNING
    db.commit()
    db.refresh(job)

    time.sleep(random.randint(2, 5))

    result = f"Processed job {job.name} successfully"

    job.result = result
    job.status = JobStatus.COMPLETED
    db.commit()
    db.refresh(job)

    cache_job_result(job.id, result)

    if isinstance(job.payload, str):
        job.payload = json.loads(job.payload)

    return job

def get_job_result(db: Session, job_id: str, user_id: str):

    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail={"error": "Job not found"}
        )

    if job.project.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail={"error": "Unauthorized access"}
        )

    cached_result = get_cached_result(job_id)

    if cached_result:
        return {"result": cached_result}

    if job.status != JobStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail={"error": "Job not completed yet"}
        )

    return {"result": job.result}