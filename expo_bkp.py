
import functools
import random
import time


class RateLimitException(Exception):
    """Custom exception simulating a 429 Too Many Requests error."""

    pass


def retry_with_backoff(
    max_retries=5,
    initial_delay=1.0,
    backoff_factor=2.0,
    jitter=True,
    exceptions=(RateLimitException,),
):
    """A retry decorator with exponential backoff and optional jitter."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = initial_delay

            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries:
                        print(
                            f"[Failed] Max retries ({max_retries}) reached. Raising error."
                        )
                        raise e

                    # Jitter prevents all concurrent clients from retrying at the exact same millisecond
                    sleep_time = current_delay
                    if jitter:
                        sleep_time += random.uniform(0, current_delay * 0.1)

                    print(
                        f"[Attempt {attempt} failed] Rate limited. Retrying in {sleep_time:.2f}s..."
                    )
                    time.sleep(sleep_time)

                    # Exponential increase: 1s -> 2s -> 4s -> 8s ...
                    current_delay *= backoff_factor

        return wrapper

    return decorator



# Dummy counter to simulate an API succeeding on the 3rd attempt
attempts_count = 0


@retry_with_backoff(max_retries=4, initial_delay=1.0, backoff_factor=2.0)
def fetch_external_data():
    global attempts_count
    attempts_count += 1

    if attempts_count < 3:
        raise RateLimitException("HTTP 429: Too Many Requests")

    return {"status": 200, "data": "Success payload received!"}


# Run test
result = fetch_external_data()
print("Final Output:", result)