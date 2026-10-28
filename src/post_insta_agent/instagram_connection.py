import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

def wait_for_container(
    container_id: str,
    max_wait: int = 300,
    poll_interval: int = 5,
) -> dict:
    """Wait until Instagram finishes processing the image."""

    deadline = time.monotonic() + max_wait
    url = f"{BASE_URL}/{container_id}"

    while time.monotonic() < deadline:
        response = requests.get(
            url,
            params={
                "fields": "status_code,status",
                "access_token": ACCESS_TOKEN,
            },
            timeout=30,
        )

        print("Container status response:", response.text)
        response.raise_for_status()

        data = response.json()
        status = data.get("status_code")

        print("Instagram container status:", status)

        if status == "FINISHED":
            return data

        if status in ("ERROR", "EXPIRED"):
            raise RuntimeError(
                f"Instagram container is {status}: {data}"
            )

        if status not in ("IN_PROGRESS", None):
            raise RuntimeError(
                f"Unexpected Instagram container status: {data}"
            )

        time.sleep(poll_interval)

    raise TimeoutError(
        f"Instagram container {container_id} was not ready "
        f"within {max_wait} seconds."
    )


ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
INSTAGRAM_USER_ID = os.getenv("INSTAGRAM_USER_ID")


BASE_URL = "https://graph.instagram.com/v25.0"


def publish_image(image_url: str, caption: str = "#motivation") -> dict:
    if not ACCESS_TOKEN or not INSTAGRAM_USER_ID:
        raise ValueError("Instagram credentials missing in .env")

    # Step 1: Create media container
    response = requests.post(
        f"{BASE_URL}/{INSTAGRAM_USER_ID}/media",
        data={
            "image_url": image_url,
            "caption": caption,
            "access_token": ACCESS_TOKEN,
        },
        timeout=60,
    )

    print("Create media status:", response.status_code)
    print("Create media response:", response.text)
    response.raise_for_status()
    
    container_id = response.json()["id"]
    print("Container created:", container_id)

    # Step 2: Wait until Instagram finishes processing
    wait_for_container(container_id)


    # Step 2: Publish media
    response = requests.post(
        f"{BASE_URL}/{INSTAGRAM_USER_ID}/media_publish",
        data={
            "creation_id": container_id,
            "access_token": ACCESS_TOKEN,
        },
        timeout=60,
    )

    print("Publish status:", response.status_code)
    print("Publish response:", response.text)
    response.raise_for_status()

    result = response.json()
    print("Instagram post published! Media ID:", result["id"])

    return result