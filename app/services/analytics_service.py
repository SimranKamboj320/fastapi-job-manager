from sqlalchemy.orm import Session
from app.models.project import Project
from app.models.job import Job, JobStatus, JobPriority

def get_user_analytics(db: Session, user_id: str):

    projects = db.query(Project).filter(Project.user_id == user_id).all()
    project_ids = [p.id for p in projects]

    jobs = db.query(Job).filter(Job.project_id.in_(project_ids)).all()

    total_projects = len(projects)
    total_jobs = len(jobs)

    completed = len([j for j in jobs if j.status == JobStatus.COMPLETED])
    failed = len([j for j in jobs if j.status == JobStatus.FAILED])
    pending = len([j for j in jobs if j.status == JobStatus.PENDING])

    high_priority = len([j for j in jobs if j.priority == JobPriority.HIGH])

    return {
        "total_projects": total_projects,
        "total_jobs": total_jobs,
        "completed": completed,
        "failed": failed,
        "pending": pending,
        "high_priority": high_priority 
    }