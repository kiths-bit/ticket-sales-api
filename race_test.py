import sys
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

import httpx


EVENT_ID = 1
SEAT_ID = int(sys.argv[1]) if len(sys.argv) > 1 else 1

URL = (
    f"http://127.0.0.1:8000"
    f"/events/{EVENT_ID}/seats/{SEAT_ID}/reserve"
)

barrier = Barrier(2)


def reserve(label):
    with httpx.Client(timeout=10) as client:
        # Make both requests wait here so they are released together.
        barrier.wait()

        response = client.post(URL)

        return (
            label,
            response.status_code,
            response.json(),
        )


def main():
    print(
        f"Concurrent reservation test "
        f"for event={EVENT_ID}, seat={SEAT_ID}"
    )

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(reserve, "Request A"),
            executor.submit(reserve, "Request B"),
        ]

        results = [future.result() for future in futures]

    for label, status_code, body in sorted(results):
        print(f"{label}: {status_code} {body}")


if __name__ == "__main__":
    main()