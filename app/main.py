from fastapi import FastAPI
from app.database import engine, Base

from app.routes import auth_routes, project_routes, job_routes, analytics_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini SaaS Job Processing System")

app.include_router(auth_routes.router)
app.include_router(project_routes.router)
app.include_router(job_routes.router)
app.include_router(analytics_routes.router)