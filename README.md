# RecruitFlow AI

A simple Applicant Tracking System (ATS) backend built with FastAPI — built as part of my application for a Vibe Coder OJT role, to practice building and shipping a real, working tool rather than a tutorial project.

## What it does

- Add new job applicants (with duplicate email protection)
- List all active applicants
- Update an applicant's status through a hiring pipeline (Pending → Interview → Hired/Rejected)
- Soft-delete applicants (hidden from the active list, but not erased from the database)
- View a live dashboard showing all active applicants in a simple HTML table

## Tech stack

- **FastAPI** — REST API framework
- **SQLModel** — ORM (built on SQLAlchemy + Pydantic)
- **SQLite** — database
- **Jinja2** — HTML templating for the dashboard

## Project structure