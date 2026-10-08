from sqlalchemy import ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)

    seats: Mapped[list["Seat"]] = relationship(
        back_populates="event",
        cascade="all, delete-orphan",
    )


class Seat(Base):
    __tablename__ = "seats"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(
        ForeignKey("events.id"),
        nullable=False,
     
    )
    seat_number: Mapped[str] = mapped_column(String(20), nullable=False)
    is_reserved: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )

    event: Mapped["Event"] = relationship(
        back_populates="seats",
    )

    order: Mapped["Order | None"] = relationship(
        back_populates="seat",
        uselist=False,
    )

    __table_args__ = (
    UniqueConstraint(
        "event_id",
        "seat_number",
        name="uq_event_seat_number",
    ),
    Index(
        "ix_seats_available_lookup",
        "event_id",
        "is_reserved",
        "id",
        "seat_number",
    ),
)


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(
        ForeignKey("events.id"),
        nullable=False,
    )
    seat_id: Mapped[int] = mapped_column(
        ForeignKey("seats.id"),
        nullable=False,
        unique=True,
    )

    seat: Mapped["Seat"] = relationship(
        back_populates="order",
    )