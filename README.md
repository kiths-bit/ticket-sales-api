# Ticket Sales API

A FastAPI backend for managing events, seats, and ticket reservations.

The project demonstrates relational data modelling, large-scale seat seeding, indexed seat availability queries, API performance, and safe concurrent reservations.

## Tech Stack

- Python 3.11
- FastAPI
- SQLAlchemy
- SQLite
- Pytest
- HTTPX

---

## Project Structure

```text
ticket-sales-api/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│   └── schemas.py
├── tests/
├── main.py
├── seed.py
├── query_plan.py
├── benchmark.py
├── race_test.py
├── ticket_sales.db
└── README.md