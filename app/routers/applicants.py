# FastAPI utilities:
#   APIRouter  — groups related endpoints under one prefix
#   Depends    — lets FastAPI inject dependencies (like DB sessions)
from app.models.applicant import ApplicantStatus
#   HTTPException — return standard HTTP error responses
from fastapi import APIRouter, Depends, HTTPException

# Session — the database session object used to run queries
from sqlmodel import Session

# get_session — our dependency that provides a database session
from app.database import get_session

# Applicant — the database model (maps to the applicants table)
from app.models.applicant import Applicant

# ApplicantCreate — the Pydantic schema that validates the request body
from app.schemas.applicant import ApplicantCreate


# Create a router instance. We'll include this in the main app later.
router = APIRouter()


@router.post("/applicants", response_model=Applicant)
def create_applicant(applicant_data: ApplicantCreate, session: Session = Depends(get_session)):
    """Create a new applicant after checking for duplicate emails."""

    # --- Duplicate email check ---
    # Query the applicants table for an existing record with the same email
    # that has NOT been soft-deleted (is_deleted == False).
    existing = session.query(Applicant).filter(
        Applicant.email == applicant_data.email,
        Applicant.is_deleted == False,
    ).first()

    # If we found a match, reject the request with HTTP 400.
    if existing is not None:
        raise HTTPException(status_code=400, detail="Email already exists")

    # --- Create the new applicant ---
    # Build an Applicant model instance from the validated request data.
    # Fields like id, status, is_deleted, and created_at get default values.
    applicant = Applicant(
        full_name=applicant_data.full_name,
        email=applicant_data.email,
        phone=applicant_data.phone,
        position=applicant_data.position,
        notes=applicant_data.notes,
    )

    # Add the new applicant to the session (pending insert).
    session.add(applicant)
    # Flush all pending changes to the database and finalise the transaction.
    session.commit()
    # Refresh the in-memory object so it reflects any DB-generated values
    # (e.g. the auto-increment id and the default created_at timestamp).
    session.refresh(applicant)

    return applicant

from typing import List
from sqlmodel import select


@router.get("/applicants", response_model=List[Applicant])
def list_applicants(session: Session = Depends(get_session)):
    """Return all applicants that haven't been soft-deleted."""

    # select() builds a query; .where() filters out deleted records
    statement = select(Applicant).where(Applicant.is_deleted == False)

    # .exec() runs it and .all() collects every matching row
    applicants = session.exec(statement).all()

    return applicants

@router.patch("/applicants/{applicant_id}/status", response_model=Applicant)
def update_status(applicant_id: int, new_status: ApplicantStatus, session: Session = Depends(get_session)):
    """Update an applicant's status (e.g. Pending -> Interview)."""

    # Fetch the applicant by primary key. Returns None if not found.
    applicant = session.get(Applicant, applicant_id)

    if applicant is None:
        raise HTTPException(status_code=404, detail="Applicant not found")

    applicant.status = new_status
    session.add(applicant)
    session.commit()
    session.refresh(applicant)

    return applicant

@router.delete("/applicants/{applicant_id}", response_model=Applicant)
def soft_delete_applicant(applicant_id: int, session: Session = Depends(get_session)):
    """Mark an applicant as deleted without removing the row from the database."""

    applicant = session.get(Applicant, applicant_id)

    if applicant is None:
        raise HTTPException(status_code=404, detail="Applicant not found")

    applicant.is_deleted = True
    session.add(applicant)
    session.commit()
    session.refresh(applicant)

    return applicant