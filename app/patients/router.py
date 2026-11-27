from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.database import get_session
from app.models import Patient

router = APIRouter(prefix="/patients", tags=["pacientes"])


class PatientIn(BaseModel):
    name: str
    email: str
    phone: str
    birthDate: date


class PatientOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    phone: str
    birthDate: date


@router.post("", status_code=status.HTTP_201_CREATED, response_model=PatientOut)
def create_patient(
    payload: PatientIn,
    request: Request,
    response: Response,
    db: Session = Depends(get_session),
) -> Patient:
    patient = Patient(
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
        birthDate=datetime.combine(payload.birthDate, datetime.min.time()),
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)

    response.headers["Location"] = str(request.url_for("get_patient", patient_id=patient.id))
    return patient


@router.get("/{patient_id}", response_model=PatientOut)
def get_patient(patient_id: int, db: Session = Depends(get_session)) -> Patient:
    patient = db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )
    return patient


@router.put("/{patient_id}", response_model=PatientOut)
def update_patient(
    patient_id: int,
    payload: PatientIn,
    db: Session = Depends(get_session),
) -> Patient:
    patient = db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )

    patient.name = payload.name
    patient.email = payload.email
    patient.phone = payload.phone
    patient.birthDate = datetime.combine(payload.birthDate, datetime.min.time())

    db.commit()
    db.refresh(patient)
    return patient


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: int, db: Session = Depends(get_session)) -> Response:
    patient = db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )

    db.delete(patient)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)