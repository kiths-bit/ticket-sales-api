import statistics
import time

import httpx


URL = "http://127.0.0.1:8000/events/1/seats/available"
REQUESTS = 20


def benchmark():
    times = []

    with httpx.Client() as client:
        # Warm-up request
        client.get(URL)

        for _ in range(REQUESTS):
            start = time.perf_counter()

            response = client.get(URL)

            elapsed_ms = (time.perf_counter() - start) * 1000

            if response.status_code != 200:
                raise RuntimeError(
                    f"Request failed: {response.status_code}"
                )

            times.append(elapsed_ms)

    print(f"Requests: {REQUESTS}")
    print(f"Min: {min(times):.2f} ms")
    print(f"Max: {max(times):.2f} ms")
    print(f"Average: {statistics.mean(times):.2f} ms")
    print(f"Median: {statistics.median(times):.2f} ms")


if __name__ == "__main__":
    benchmark()