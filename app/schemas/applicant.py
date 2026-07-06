# Optional: allows fields to be left empty (None)
from typing import Optional

# SQLModel: base class for our request/response models
# (When used without table=True, SQLModel behaves like a Pydantic model)
from sqlmodel import SQLModel


class ApplicantCreate(SQLModel):
    """Schema for creating a new applicant.
    
    This defines what the client must (or may) send in the
    request body when POSTing a new applicant. Fields like
    id, status, created_at, and is_deleted are set by the
    server automatically and should not be provided by the client.
    """

    full_name: str
    # The applicant's full name (required)

    email: str
    # The applicant's email address (required)

    phone: Optional[str] = None
    # Phone number — not required, defaults to None

    position: str
    # The job position the applicant applied for (required)

    notes: Optional[str] = None
    # Internal notes — not required, defaults to None
