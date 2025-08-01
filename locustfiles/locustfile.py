import sys
import os
from locust import HttpUser, task, events, between

# Add the parent directory to the Python path to find the configurations module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Configurations.auth import Authentication
from configurations.utils import load_json_payload

# Global variable to hold the auth token
token = None


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """
    This event listener runs once at the beginning of the test.
    It fetches the authentication token and stores it in a global variable.
    If the token fetch fails, the test will be stopped.
    """
    global token
    print("[locust file] Fetching authentication token...")
    auth = Authentication(
        base_url=os.getenv("BASE_URL"),
        username=os.getenv("USER_NAME"),
        password=os.getenv("PASSWORD")
    )

    token = auth.get_auth_token()
    if not token:
        print("[locust file] FATAL: Could not get auth token. Stopping test.")
        # Stop the test if authentication fails
        environment.runner.quit()
    else:
        print(f"[locust file] Token received successfully.")


class RestfulBookerUser(HttpUser):
    """
    User class that simulates a user interacting with the Restful Booker API.
    """
    # Each user will wait between 1 and 3 seconds between tasks
    wait_time = between(1, 3)

    # The host to test against
    #host = "https://restful-booker.herokuapp.com"

    def on_start(self):
        """
        on_start is called when a Locust user starts.
        We set the required headers for all subsequent requests here.
        """
        # The token is fetched once globally, and each user sets it in its headers.
        if token:
            self.client.headers.update({
                "Content-Type": "application/json",
                "Accept": "application/json",
                # The API expects the token in a cookie named 'token'
                "Cookie": f"token={token}"
            })
        # We will also store the booking_id for this specific user session
        # self.booking_id = None

    @task(1)
    def health_check(self):
        """Task to check if the API is up and running."""
        self.client.get("/ping", name="/ping")

    @task(5)  # This task will be executed 5 times more often than the health_check
    def booking_lifecycle(self):
        """
        Simulates a full user workflow:
        1. Create a booking.
        2. Get details of the created booking.
        3. Update booking.
        4. Delete booking.
        """
        # --- 1. Create a booking --- #
        create_payload = load_json_payload("createBooking.json")
        with self.client.post(
                "/booking",
                json=create_payload,
                name="/booking [create]",
                catch_response=True
        ) as response:
            if response.status_code == 200:
                try:
                    self.booking_id = response.json()["bookingid"]
                    response.success()
                    print(f"Created booking with ID: {self.booking_id}")
                except KeyError:
                    response.failure("Response did not contain booking_id")
                    return
            else:
                response.failure(f"Failed to create booking, status code: {response.status_code}")
                return

        # --- 2. Get the created booking --- #
        with self.client.get(
            f"/booking/{self.booking_id}",
            name="/booking/{id} [get]",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
                print(f"Got booking with ID: {self.booking_id}")
            else:
                response.failure("Load to get booking information")


        # --- 3. Update the booking --- #
        update_payload = load_json_payload("updateBooking.json")
        #RestfulBooker use PUT method to update the booking, Preferred method PATCH
        with self.client.put(
            f"/booking/{self.booking_id}",
            json=update_payload,
            name="/booking/{id} [put]",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
                print(f"Updated booking with ID: {self.booking_id}")
            else:
                response.failure("Fail to update booking information")


        # --- 4. Delete the booking --- #
        with self.client.delete(
                f"/booking/{self.booking_id}",
                name="/booking/{id} [delete]",
                catch_response=True
        ) as response:
            if response.status_code == 201: # This API response 201 for valid delete operation, Preferred status code 200
                response.success()
                print(f"Deleted booking with ID: {self.booking_id}")
            else:
                response.failure("Fail to delete booking information")

        # self.booking_id = None  # Reset for the next run
