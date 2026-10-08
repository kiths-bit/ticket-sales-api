from app.database import Base, SessionLocal, engine
from app.models import Event, Seat


EVENT_COUNT = 10
SEATS_PER_EVENT = 1000


def seed_database():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Avoid creating duplicate seed data if the script is run again.
        existing_events = db.query(Event).count()

        if existing_events > 0:
            print("Database already contains events. Nothing to seed.")
            return

        events = []

        for event_number in range(1, EVENT_COUNT + 1):
            event = Event(
                name=f"Concert Event {event_number}"
            )
            events.append(event)

        db.add_all(events)
        db.flush()

        seats = []

        for event in events:
            for seat_number in range(1, SEATS_PER_EVENT + 1):
                seats.append(
                    Seat(
                        event_id=event.id,
                        seat_number=f"S{seat_number}",
                        is_reserved=False,
                    )
                )

        db.add_all(seats)
        db.commit()

        print(f"Created {len(events)} events.")
        print(f"Created {len(seats)} seats.")
        print(
            f"Total seats: {EVENT_COUNT * SEATS_PER_EVENT}"
        )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()