from sqlalchemy.orm import Session
from models.job import Job, JobStatus
from schemas.job_schema import JobCreate

def create_job(db: Session, job: JobCreate, project_id: int):
    new_job = Job(
        name=job.name,
        payload=job.payload,
        priority=job.priority,
        project_id=project_id
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job

def get_job_by_id(db: Session, job_id: str):
    return db.query(Job).filter(Job.id == job_id).first()

def get_jobs_by_project(db: Session, project_id: int):
    return db.query(Job).filter(Job.project_id == project_id).all()

def get_jobs(
    db: Session,
    project_id: int,
    status: str = None,
    priority: str = None,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "created_at",
    order: str = "asc"
):
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

    return query.offset((page - 1) * limit).limit(limit).all()

def update_job_status(db: Session, job_id: str, status: JobStatus):
    job = get_job_by_id(db, job_id)

    if job:
        job.status = status
        db.commit()
        db.refresh(job)

    return job

def update_job_result(db: Session, job_id: str, result: str):
    job = get_job_by_id(db, job_id)

    if job:
        job.result = result
        job.status = JobStatus.COMPLETED
        db.commit()
        db.refresh(job)

    return job

def delete_job(db: Session, job_id: str):
    job = get_job_by_id(db, job_id)

    if job:
        db.delete(job)
        db.commit()

    return job