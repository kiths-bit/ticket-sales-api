from sqlalchemy import text

from app.database import SessionLocal


def show_query_plan():
    db = SessionLocal()

    try:
        query = """
        EXPLAIN QUERY PLAN
        SELECT id, seat_number
        FROM seats
        WHERE event_id = 1
          AND is_reserved = 0
        ORDER BY id;
        """

        rows = db.execute(text(query)).fetchall()

        print("QUERY PLAN")
        print("----------")

        for row in rows:
            print(row)

    finally:
        db.close()


if __name__ == "__main__":
    show_query_plan()