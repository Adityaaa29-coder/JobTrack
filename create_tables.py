
from app.db.database import Base, engine
from app.models import JobApplication

Base.metadata.create_all(bind=engine)

print("JobTrack tables created successfully!")
