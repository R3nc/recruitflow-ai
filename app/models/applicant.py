# datetime: used to automatically set the created_at timestamp
from datetime import datetime

# Enum: lets us define a fixed set of allowed status values
from enum import Enum

# Optional: indicates a field can be left as None (not required)
from typing import Optional

# SQLModel: base class for our database model
# Field: lets us add extra options to each column (e.g. unique, default)
from sqlmodel import SQLModel, Field


class ApplicantStatus(str, Enum):
    """The possible stages an applicant can be in during the hiring process."""

    PENDING = "Pending"    # Application received, not reviewed yet
    INTERVIEW = "Interview"  # Candidate is being interviewed
    HIRED = "Hired"        # Candidate has been hired
    REJECTED = "Rejected"  # Candidate was not selected


class Applicant(SQLModel, table=True):
    """Represents a single job applicant stored in the database."""

    id: Optional[int] = Field(default=None, primary_key=True)
    # Auto-generated unique identifier for each applicant

    full_name: str
    # The applicant's full name (required)

    email: str = Field(unique=True)
    # Email address — must be unique across all applicants

    phone: Optional[str] = None
    # Phone number (optional, defaults to None if not provided)

    position: str
    # The job position the applicant applied for (required)

    status: ApplicantStatus = Field(default=ApplicantStatus.PENDING)
    # Current stage in the hiring pipeline (defaults to "Pending")

    notes: Optional[str] = None
    # Any internal notes or comments about the applicant (optional)

    is_deleted: bool = False
    # Soft-delete flag. When True, the record is treated as deleted
    # without actually removing it from the database.

    created_at: datetime = Field(default_factory=datetime.utcnow)
    # Timestamp set automatically when the applicant is first created
