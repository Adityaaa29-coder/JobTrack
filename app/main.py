from fastapi.middleware.cors import CORSMiddleware
from datetime import date

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models import JobApplication

app = FastAPI(
    title="JobTrack API",
    description="Job application and placement analytics platform",
    version="0.2.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "https://jobtrack-frontend-fpi7.onrender.com",
],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class JobApplicationCreate(BaseModel):
    company_name: str = Field(min_length=1, max_length=150)
    job_role: str = Field(min_length=1, max_length=150)
    status: str = "Applied"
    applied_date: date = Field(default_factory=date.today)


class JobApplicationResponse(BaseModel):
    id: int
    company_name: str
    job_role: str
    status: str
    applied_date: date

    model_config = ConfigDict(from_attributes=True)


class JobApplicationUpdate(BaseModel):
    company_name: str | None = Field(
        default=None, min_length=1, max_length=150
    )
    job_role: str | None = Field(
        default=None, min_length=1, max_length=150
    )
    status: str | None = None
    applied_date: date | None = None



@app.get("/")
def home():
    return {
        "message": "Welcome to JobTrack API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "JobTrack",
    }


@app.post(
    "/applications",
    response_model=JobApplicationResponse,
    status_code=201,
)
def create_application(
    application: JobApplicationCreate,
    db: Session = Depends(get_db),
):
    allowed_statuses = {"Applied", "Interview", "Rejected", "Offer"}

    if application.status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Status must be Applied, Interview, Rejected, or Offer",
        )

    new_application = JobApplication(**application.model_dump())
    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application


@app.get(
    "/applications",
    response_model=list[JobApplicationResponse],
)
def list_applications(db: Session = Depends(get_db)):
    return (
        db.query(JobApplication)
        .order_by(JobApplication.id.desc())
        .all()
    )


@app.patch(
    "/applications/{application_id}",
    response_model=JobApplicationResponse,
)
def update_application(
    application_id: int,
    updates: JobApplicationUpdate,
    db: Session = Depends(get_db),
):
    application = db.get(JobApplication, application_id)

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    update_data = updates.model_dump(exclude_unset=True)

    if "status" in update_data:
        allowed_statuses = {
            "Applied", "Interview", "Rejected", "Offer"
        }

        if update_data["status"] not in allowed_statuses:
            raise HTTPException(
                status_code=400,
                detail="Status must be Applied, Interview, Rejected, or Offer",
            )

    for field, value in update_data.items():
        setattr(application, field, value)

    db.commit()
    db.refresh(application)

    return application

@app.delete("/applications/{application_id}")
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
):
    application = db.get(JobApplication, application_id)

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    db.delete(application)
    db.commit()

    return {
        "message": "Application deleted successfully",
        "id": application_id,
    }

@app.get("/analytics")
def get_analytics(db: Session = Depends(get_db)):
    applications = db.query(JobApplication).all()

    total = len(applications)
    interviews = sum(
        app.status == "Interview" for app in applications
    )
    rejected = sum(
        app.status == "Rejected" for app in applications
    )
    offers = sum(
        app.status == "Offer" for app in applications
    )
    applied = sum(
        app.status == "Applied" for app in applications
    )

    return {
        "total_applications": total,
        "applied": applied,
        "interviews": interviews,
        "rejected": rejected,
        "offers": offers,
        "offer_rate_percent": round(
            (offers / total * 100) if total else 0, 2
        ),
    }
