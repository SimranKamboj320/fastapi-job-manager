from sqlalchemy.orm import Session
from models.project import Project
from schemas.project_schema import ProjectCreate

def create_project(db: Session, user_id: int, project: ProjectCreate):
    new_project = Project(
        name=project.name,
        description=project.description,
        user_id=user_id
    ) 

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project

def get_project_by_user_id(db: Session, user_id: int):
    return db.query(Project).filter(Project.user_id == user_id).all()

def get_project_by_project_id(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()

def delete_project(db: Session, project_id: int):
    project = get_project_by_project_id(db, project_id)
    if project:
        db.delete(project)
        db.commit()
        return project