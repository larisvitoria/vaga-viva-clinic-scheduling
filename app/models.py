from datetime import datetime

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(120))
    phone: Mapped[str] = mapped_column(String(20))
    birthdate: Mapped[datetime]


class Professional(Base):
    __tablename__ = "professionals"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    specialty: Mapped[str] = mapped_column(String(80))


class Appointment(Base):
    __tablename__ = "appointments"
    __table_args__ = (Index("appointments_professional_id_starts_at_idx", "professional_id", "starts_at"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    professional_id: Mapped[int] = mapped_column(ForeignKey("professionals.id"))
    patient_id: Mapped[int]
    starts_at: Mapped[datetime]
    duration_minutes: Mapped[int]
