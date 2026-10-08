from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app import models
from app.database import Base, SessionLocal, engine
from app.schemas import AvailableSeatsResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ticket Sales API")


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Ticket Sales API is running"}


@app.get(
    "/events/{event_id}/seats/available",
    response_model=AvailableSeatsResponse,
)
def get_available_seats(
    event_id: int,
    db: Session = Depends(get_db),
):
    event = db.get(models.Event, event_id)

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found",
        )

    statement = (
        select(models.Seat)
        .where(
            models.Seat.event_id == event_id,
            models.Seat.is_reserved.is_(False),
        )
        .order_by(models.Seat.id)
    )

    seats = db.scalars(statement).all()

    return {
        "event_id": event_id,
        "available_seats": [
            {
                "id": seat.id,
                "seat_number": seat.seat_number,
            }
            for seat in seats
        ],
    }


@app.post("/events/{event_id}/seats/{seat_id}/reserve")
def reserve_seat(
    event_id: int,
    seat_id: int,
    db: Session = Depends(get_db),
):
    statement = (
        update(models.Seat)
        .where(
            models.Seat.id == seat_id,
            models.Seat.event_id == event_id,
            models.Seat.is_reserved.is_(False),
        )
        .values(is_reserved=True)
    )

    result = db.execute(statement)

    if result.rowcount == 0:
        db.rollback()

        seat_exists = db.scalar(
            select(models.Seat.id).where(
                models.Seat.id == seat_id,
                models.Seat.event_id == event_id,
            )
        )

        if seat_exists is None:
            raise HTTPException(
                status_code=404,
                detail="Seat not found",
            )

        raise HTTPException(
            status_code=409,
            detail="Seat already reserved",
        )

    order = models.Order(
        event_id=event_id,
        seat_id=seat_id,
    )

    db.add(order)

    try:
        db.commit()
    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Seat could not be reserved",
        )

    return {
        "message": "Seat reserved successfully",
        "event_id": event_id,
        "seat_id": seat_id,
        "order_id": order.id,
    }