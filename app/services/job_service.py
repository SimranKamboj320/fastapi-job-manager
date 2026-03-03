from sqlalchemy.orm import Session
from models.job import Job, JobStatus
from models.project import Project
from schemas.job_schema import JobCreate, StatusEnum, PriorityEnum
from fastapi import HTTPException
from utils.redis_service import check_rate_limit, cache_job_result, get_cached_result
import json
import time
import random


# 🔹 CREATE JOB (WITH OWNERSHIP CHECK)
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
        payload=json.dumps(job.payload),  # store JSON string
        priority=job.priority,
        project_id=project_id
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    # convert back for response
    new_job.payload = json.loads(new_job.payload)

    return new_job


# 🔹 GET JOB BY ID
def get_job_by_id(db: Session, job_id: str):
    job = db.query(Job).filter(Job.id == job_id).first()

    if job:
        job.payload = json.loads(job.payload)

    return job


# 🔹 LIST JOBS WITH FILTER + PAGINATION + SORTING
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

    # Ownership check
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

    # Decode payload before returning
    for job in jobs:
        job.payload = json.loads(job.payload)

    return jobs


# 🔹 DELETE JOB (WITH OWNERSHIP CHECK)
def delete_job(db: Session, job_id: str, user_id: str):

    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail={"error": "Job not found"}
        )

    if job.project.owner.id != user_id:
        raise HTTPException(
            status_code=403,
            detail={"error": "Unauthorized access"}
        )

    db.delete(job)
    db.commit()

    return {"message": "Job deleted successfully"}


# 🔹 EXECUTE JOB
def execute_job(db: Session, job_id: str, user_id: str):

    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail={"error": "Job not found"}
        )

    if job.project.owner.id != user_id:
        raise HTTPException(
            status_code=403,
            detail={"error": "Unauthorized access"}
        )

    # Rate limit check
    check_rate_limit(user_id)

    # Update status → RUNNING
    job.status = JobStatus.RUNNING
    db.commit()
    db.refresh(job)

    # Simulate processing (2–5 seconds)
    time.sleep(random.randint(2, 5))

    result = f"Processed job {job.name} successfully"

    # Update status → COMPLETED
    job.result = result
    job.status = JobStatus.COMPLETED
    db.commit()
    db.refresh(job)

    # Cache result (TTL = 300 seconds)
    cache_job_result(job.id, result)

    job.payload = json.loads(job.payload)

    return job


# 🔹 GET JOB RESULT (WITH REDIS CACHE)
def get_job_result(db: Session, job_id: str, user_id: str):

    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail={"error": "Job not found"}
        )

    if job.project.owner.id != user_id:
        raise HTTPException(
            status_code=403,
            detail={"error": "Unauthorized access"}
        )

    # Check Redis first
    cached = get_cached_result(job_id)

    if cached:
        return {"result": cached}

    if job.status != JobStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail={"error": "Job not completed yet"}
        )

    return {"result": job.result}