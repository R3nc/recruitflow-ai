from fastapi import FastAPI, Depends, Request
from app.database import create_db_and_tables
from app.models import Applicant
from app.routers import applicants

from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from app.database import get_session
# 1. Create app FIRST

app = FastAPI(
    title="RecruitFlow AI",
    version="1.0.0",
)

templates = Jinja2Templates(directory="templates")

# 2. THEN include the router
app.include_router(applicants.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "RecruitFlow AI API is running"}

@app.get("/dashboard")
def dashboard(request: Request, session: Session = Depends(get_session)):
    """Render an HTML page showing all active applicants."""

    statement = select(Applicant).where(Applicant.is_deleted == False)
    applicants = session.exec(statement).all()

    return templates.TemplateResponse(
    request,
    "dashboard.html",
    {"applicants": applicants}
)

