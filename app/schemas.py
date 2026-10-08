from pydantic import BaseModel


class AvailableSeat(BaseModel):
    id: int
    seat_number: str


class AvailableSeatsResponse(BaseModel):
    event_id: int
    available_seats: list[AvailableSeat]