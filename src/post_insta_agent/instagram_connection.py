import os
import requests
from dotenv import load_dotenv

load_dotenv()

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